from rest_framework import permissions
from rest_framework import mixins, viewsets
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Student, Teacher, User
from .serializers import ProfileSerializer, StudentRegistrationSerializer, TeacherRegistrationSerializer, UserSerializer



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



class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=204)


class UploadImage(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        # request.data['student'] = request.user.id 
        # assignment_file = request.FILES['file']
        # print("_______________________________________________________________") 
        # print(request.FILES)
        try:
            request.data['image'] = request.FILES['image'] 
            serializer = ProfileSerializer(data = request.data)
        except: 
            serializer = ProfileSerializer(data = request.data)
 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
