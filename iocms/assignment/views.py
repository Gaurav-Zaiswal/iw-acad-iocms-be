from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import CreateView
from rest_framework import serializers
from users.models import User


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import Teacher, Student
from users.permissions import IsStudentUser, IsTeacherUser
from classroom.models import ClassroomStudents
from .models import Assignment, AssignmentByStudent 
from .serializers import (AssignmentCreateSerializer, 
                            AssignmentListSerializer, 
                            AssignmentDetailSerializer,
                            AssignmentSubmitSerializer)
from .send_email import send_email
# Create your views here.



class AssignmentListView(APIView):
    permission_classes = [IsStudentUser]   

    def get(self, request,class_pk, **kwargs):

        query = Assignment.objects.filter(class_name = class_pk)
        serializer_context = {
            'request': request,
        }

        serializer = AssignmentListSerializer(query,context = serializer_context, many = True)
        print(request.user.pk)
        return Response(serializer.data)


class AssignmentCreateView(APIView):

    permission_classes = [IsTeacherUser]

    def post(self, request, class_pk):
        request.data['teacher'] = request.user.id
        classroom_id = self.kwargs['class_pk']
        request.data['class_name'] = classroom_id
        print('Kwragssss: :: ', self.kwargs) 
        serializer = AssignmentCreateSerializer(data = request.data)

        # print(request.data)
        if serializer.is_valid():
            # user = get_object_or_404(User, id = request.user.id)
            # print(user.email)
            # serializer.validated_data['teacher'] = request.user.id
            print(serializer.validated_data)
            serializer.save()  

            #Part for sending email to notify students about new assignment after it get posted
            enrolled_students = ClassroomStudents.objects.get(classroom_id =classroom_id )
            send_email(request, Assignment,enrolled_students,serializer)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#assignment detail
class AssignmentDetailView(APIView):
    # lookup_field = 'assignment_pk'

    permission_classes = [IsStudentUser]    
     
    def get(self, request,  pk):
        query = Assignment.objects.get(id = pk) 
        serializer = AssignmentDetailSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)


#assignment submit by student
class AssignmentSubmitView(APIView):
    permission_classes = [IsStudentUser]   

    def get(self, requst, pk):
        query  = get_object_or_404(Assignment,pk = pk)
        serializer = AssignmentDetailSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,pk):
        request.data['student'] = request.user.id 
        request.data['assignment_details'] = pk

        serializer = AssignmentSubmitSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class SubbmittedAssignmentView(APIView):
    permission_classes = [IsTeacherUser]

    def get(self,request, class_pk):

        query = AssignmentByStudent.objects.filter(assignment_details__teacher= self.request.user.id)
        serializer = AssignmentSubmitSerializer(query, many = True)

        return Response(serializer.data, status=status.HTTP_200_OK)