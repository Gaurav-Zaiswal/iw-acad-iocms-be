from rest_framework import permissions
from rest_framework import mixins, viewsets
from rest_framework import generics

from .models import Student, Teacher
from .serializers import StudentRegistrationSerializer, TeacherRegistrationSerializer


class CreateStudentView(generics.CreateAPIView,
                        viewsets.GenericViewSet):

    model = Student
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = StudentRegistrationSerializer


class CreateTeacherView(generics.CreateAPIView,
                        viewsets.GenericViewSet):

    model = Teacher
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TeacherRegistrationSerializer
