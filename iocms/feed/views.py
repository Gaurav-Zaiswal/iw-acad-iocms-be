from django.shortcuts import render

from django.http import Http404
from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from users.permissions import IsTeacherUser, IsStudentUser
from users.models import User

from .models import Classroom, ClassroomStudents
from .serializers import ClassroomFeedCreateSerializer, ClassroomFeedDetailSerializer, ClassroomFeedListSerializer \



class FeedCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = ClassroomFeedCreateSerializer(data=request.data)
        request.data['posted_by'] = request.user.id
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

