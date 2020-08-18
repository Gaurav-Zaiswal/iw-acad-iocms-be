from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView
from rest_framework import request
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Assignment, Teacher 
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
        print(query)
        return Response(serializer.data)

    def post(self, request):
        serializer = AssignmentCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
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

