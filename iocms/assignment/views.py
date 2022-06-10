from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied

from django.http import Http404
from django.views.generic import CreateView
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import User, Teacher, Student
from users.views import UserView
from users.permissions import IsStudentUser, IsTeacherUser
from classroom.models import ClassroomStudents
from .models import Assignment, AssignmentByStudent 
from .serializers import (AssignmentCreateSerializer, 
                            AssignmentListSerializer, 
                            AssignmentDetailSerializer,
                            AssignmentSubmitSerializer)
# from .send_email import send_email

# Create your views here.



class AssignmentListView(APIView):
    # permission_classes = [IsStudentUser]   
    permission_classes = [
        permissions.IsAuthenticated, 
    ]
    def get(self, request,class_pk, **kwargs):
        query = Assignment.objects.filter(class_name = class_pk)

        serializer_context = {
            'request': request,
        }

        serializer = AssignmentListSerializer(query,context = serializer_context, many = True)
        
        return Response(serializer.data)

   

class AssignmentCreateView(APIView):

    # permission_classes = [IsTeacherUser]

    def post(self, request, class_pk):
        request.data['teacher'] = request.user.id
        request.data['class_name'] = class_pk

        serializer = AssignmentCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()             
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#assignment detail
class AssignmentDetailView(APIView):
    # lookup_field = 'assignment_pk'

    # permission_classes = [IsStudentUser]    
     
    def get(self, request,  pk):
        query = Assignment.objects.get(id = pk) 
        serializer = AssignmentDetailSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)


#assignment submit by student
class AssignmentSubmitView(APIView):
    permission_classes = [IsAuthenticated,] 
    # parser_classes = [MultiPartParser,FileUploadParser, ]  

    def get(self, requst, pk):
        query  = get_object_or_404(Assignment,pk = pk)
        serializer = AssignmentDetailSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,pk):
        request.data['student'] = request.user.id 
        # assignment_file = request.FILES['file'] 
        print(request.data)
        try:
            request.data['assignment_answer'] = request.FILES['file'] 
            serializer = AssignmentSubmitSerializer(data = request.data)
        except: 
            serializer = AssignmentSubmitSerializer(data = request.data)
 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class SubbmittedAssignmentView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self,request, class_pk):
        if request.user.is_teacher:
            # print()
            # query = AssignmentByStudent.objects.filter(assignment_details__teacher= 1)   #original query
            query = AssignmentByStudent.objects.filter(assignment_details__class_name__id=class_pk) # updated query
            serializer = AssignmentSubmitSerializer(query, many = True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied('You dont have access to view this data ')
