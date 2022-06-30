import json

from django.db.models import Avg
from django.http import Http404, JsonResponse
from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 

from users.permissions import IsTeacherUser, IsStudentUser
from users.models import User

from .models import Classroom, ClassroomStudents, Rating
from .serializers import ClassroomCreateSerializer, ClassroomDetailSerializer, ClassroomListSerializer, \
    ClassroomAddSerializer


class ClassroomView(APIView):

    def get(self, request, **kwargs):
        query = Classroom.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = ClassroomListSerializer(query, context=serializer_context, many=True)

        return Response(serializer.data)


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
class ClassroomDetailView(APIView):
    permission_classes = [IsAuthenticated,]

    def get_object(self, pk):
        try:
            return Classroom.objects.get(pk=pk)
        except Classroom.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializer = ClassroomDetailSerializer(query)
        print(serializer.data['created_by'])
        
        return Response(serializer.data, status=status.HTTP_200_OK)
       

# Classroom List
class ClassroomListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        
        user = User.objects.get(id = user_id) 
        if user.is_teacher:
            query = Classroom.objects.filter(created_by_id=user_id)
            serializer = ClassroomListSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # query for list of class where student is enrolled
            enrolled_student = ClassroomStudents.objects.filter(enrolled_student_id__in=[user.id])
            # example O/P from above <QuerySet [<ClassroomStudents: class12>, <ClassroomStudents: class1>,
            # <ClassroomStudents: New class >]>
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


class Top10Classrooms(APIView):

    def get(self, request):
        qs = Rating.objects.values('classroom').annotate(avg_rating=Avg('rating'))[:10]
        return JsonResponse()