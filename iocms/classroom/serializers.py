from rest_framework import serializers

from .models import Classroom, ClassroomStudents


class ClassroomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'class_description', 'created_by']


class ClassroomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"


class ClassroomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'class_description', 'created_by']


class ClassroomAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomStudents
        fields = "__all__"
