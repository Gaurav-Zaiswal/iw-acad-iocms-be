from django.shortcuts import render

from django.http import Http404
from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import ClassroomFeedCreateSerializer, ClassroomFeedDetailSerializer, ClassroomFeedListSerializer \

from .models import ClassroomFeed


class FeedView(APIView):
    def get(self, request, **kwargs):
        query = ClassroomFeed.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = ClassroomFeedListSerializer(query, context=serializer_context, many=True)

        return Response(serializer.data)


class FeedCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, class_id):
        serializer = ClassroomFeedCreateSerializer(data=request.data)
        request.data['posted_by'] = request.user.id 
        print(request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassroomFeedDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, pk):
        try:
            return ClassroomFeed.objects.get(pk=pk)
        except ClassroomFeed.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializer = ClassroomFeedDetailSerializer(query)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id):

        query = ClassroomFeed.objects.filter(classroom_id = class_id) 
        serializer = ClassroomFeedListSerializer(query, many=True)
        return Response(serializer.data)


# class FeedListView(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#
#     def list(self, request):
#         query = ClassroomFeed.objects.all()
#         serializer = ClassroomFeedListSerializer(query, many=True)
#         return serializer


