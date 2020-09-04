from rest_framework import permissions
from rest_framework import mixins, viewsets
from rest_framework import generics

from .models import Student, Teacher, User
from .serializers import StudentRegistrationSerializer, TeacherRegistrationSerializer, UserSerializer


CURRENT_USER = {}

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


class UserView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated, 
    ]
    model = User 

    serializer_class = UserSerializer 

    def get_object(self):
        return self.request.user

