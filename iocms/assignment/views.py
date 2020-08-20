from re import sub
from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView

from django.core.mail import send_mail #To send email
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from classroom.settings import EMAIL_HOST_USER
from .models import Assignment, Student, Teacher 
from .serializers import (AssignmentCreateSerializer, 
                            AssignmentListSerializer, 
                            AssignmentDetailSerializer,
                            AssignmentSubmitSerializer)
# Create your views here.



class AssignmentView(APIView):
    def get(self, request, **kwargs):
        query = Assignment.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = AssignmentListSerializer(query,context = serializer_context, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AssignmentCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()

            #Part for sending email to notify students about new assignment after it get posted
            id_of_new_assignemnt = serializer.data["id"]
            new_assignment_data = Assignment.objects.get(id=id_of_new_assignemnt)
            student_email_list = []
            for student in Student.objects.all():
                student_email_list.append(student.email)
            email_subject = f'New assignment posted by {new_assignment_data.teacher}'
            current_site = get_current_site(request)

            html_message = render_to_string('assignment/email_template/email.html',{
                'teacher' : new_assignment_data.teacher,
                'deadline' : new_assignment_data.deadline,
                'domain' : current_site.domain,
                'pk' : id_of_new_assignemnt,
            })
            message = strip_tags(html_message)
            send_mail(subject=email_subject, message=message,from_email=EMAIL_HOST_USER, recipient_list=student_email_list, html_message= html_message)
            
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#assignment detail
class AssignmentDetailView(APIView):
     
    def get_object(self, pk):
        try:
            return  Assignment.objects.get(pk = pk)
        except Assignment.DoesNotExist:
            raise Http404
    
    def get(self, request,  pk):
        query = self.get_object(pk)
        serializer = AssignmentDetailSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)


#assignment submit by student
class AssignmentSubmitView(APIView):
    def post(self, request):
        serializer = AssignmentSubmitSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

