from rest_framework import serializers
from rest_framework import response

from .models import Classroom, ClassroomStudents
from users.serializers import UserSerializer, TeacherSerializer, StudentSerializer


class ClassroomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'class_description', 'created_by']
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['created_by'] = UserSerializer(instance.created_by).data
        return response 
    
class ClassroomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['created_by'] = UserSerializer(instance.created_by).data
        return response 

class ClassroomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'class_description','class_code', 'created_by', ] 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['created_by'] = TeacherSerializer(instance.created_by).data
        return response 

class ClassroomAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomStudents
        fields = "__all__"
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['enrolled_student_id'] = StudentSerializer(instance.enrolled_student_id).data
        return response 
