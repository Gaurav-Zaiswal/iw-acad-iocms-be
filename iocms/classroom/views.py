from django.db.models import Avg 
from django.http import Http404, JsonResponse
from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated 

from users.permissions import IsStudentUser
from custom_mixing import PaginationMixing
from custom_pagination import CustomPageNumberPagination
from users.models import User

from .models import Classroom, ClassroomStudents, Rating
from .serializers import ClassroomCreateSerializer, ClassroomDetailSerializer, ClassroomListSerializer, \
    ClassroomAddSerializer, RatingSerializer, TopRatedClassSerializer, ClassroomSearchSerializer



class ClassroomView(APIView, PaginationMixing):
    pagination_class = CustomPageNumberPagination

    def get(self, request, **kwargs):
        query = Classroom.objects.all()
        page = self.paginate_queryset(query)
        serializer = ClassroomListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class ClassroomCreateView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        if request.user.is_teacher:
            serializer = ClassroomCreateSerializer(data=request.data)
            request.data['created_by'] = request.user.id
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied('Only teacher can create class')

# Classroom detail
class ClassroomDetailView(RetrieveAPIView):
    # used generic API so that I could utilize get_serializer_context() method
    # to add additional data in context
    queryset = Classroom.objects.all()  # need to retrieve one object, but still have to fetch all objects, why?!
    serializer_class = ClassroomDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        clsrm_obj = self.get_object()  # get the classroom instance
        no_of_ratings = clsrm_obj.classroom.count()  # here classroom is related_name field
        avg_rating = clsrm_obj.classroom.values('rating').aggregate(avg_rating=Avg('rating'))
        # add two more k-v into context dict
        context.update(
            {
                'no_of_ratings': no_of_ratings,
                'avg_rating': avg_rating
            }
        )
        return context

# Classroom List
class ClassroomListView(APIView, PaginationMixing):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_teacher:
            query = Classroom.objects.filter(created_by_id=user_id)
            page = self.paginate_queryset(query)
            # print(page)
            serializer = ClassroomListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)  # from PaginationMixing
            # return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # query for list of class where student is enrolled
            enrolled_student = ClassroomStudents.objects.filter(enrolled_student_id__in=[user.id])
            print(enrolled_student)
            # query to extract Classroom model fields by passing classroom_id
            student_enrolled_class_list = [classroom.classroom_id for classroom in enrolled_student]
            serializer = ClassroomListSerializer(student_enrolled_class_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class ClassroomAddView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        query = request.data["class_code"]
        serializer = ClassroomAddSerializer(data=request.data)
        classroom = Classroom.objects.get(class_code=query)  # Getting information of the class
        current_user_id = request.user.id
        if classroom.is_class_code_enabled:
            request.data['classroom_id'] = classroom.id
            try:
                classroomStudent = ClassroomStudents.objects.get(classroom_id=classroom.id)
            except ClassroomStudents.DoesNotExist:
                classroomStudent = None

            if classroomStudent is None:
                request.data['enrolled_student_id'] = [current_user_id, ]
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:

                list_of_enrolled_student = classroomStudent.enrolled_student_id.all()  # Find enrolled students
                list_of_enrolled_student_id = [student.user.id for student in
                                               list_of_enrolled_student]  # Collect students' id

                if current_user_id in list_of_enrolled_student_id:
                    return Response({"message": "student already joined", "email": request.user.email},
                                    status=status.HTTP_201_CREATED)
                else:
                    classroomStudent.enrolled_student_id.add(current_user_id)
                    return Response({"message": "Student joined to class successfully", "email": request.user.email},
                                    status=status.HTTP_201_CREATED)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("You do not have permission to view classes of other users.")

class TopRatedClassrooms(APIView, PaginationMixing):
    """
    returns top rated classrooms on the basis of average rating given by students
    """
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        qs = Rating.objects.select_related('classroom').values(
            'classroom__class_name', 'classroom__id', 'classroom__class_description', 'classroom__created_by').annotate(
            avg_rating=Avg('rating'))
        page = self.paginate_queryset(qs)
        serializer = TopRatedClassSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)  # from PaginatedMixing

class RateClassroom(APIView):
    #allow only students to access
    #student can rate a class (if he/she is enrolled in it)

    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, IsStudentUser]   
    
    def post(self, request, pk):
        if request.user.is_student:
            serializer = RatingSerializer(data=request.data)
            request.data['rated_by'] = request.user.id # hopefully its student's id
            request.data['classroom'] = pk
            print(request.data)
            if serializer.is_valid():
                serializer.save()        
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied('Only teacher can create class')


class Lookup(ListAPIView):
    """
    a normal Django search (using filter)
    """
    serializer_class = ClassroomSearchSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        q = self.kwargs['q']
        return Classroom.objects.filter(class_name__icontains=q)
