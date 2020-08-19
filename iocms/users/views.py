from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .models import Student, Teacher
from .serializers import StudentRegisterSerializer


class CreateStudentView(CreateAPIView):

    model = Student
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = StudentRegisterSerializer


