from rest_framework import serializers
from rest_framework import response

from .models import Classroom, ClassroomStudents
from users.serializers import UserSerializer, TeacherSerializer, StudentSerializer


class ClassroomFeedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomFeed
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['posted_by'] = TeacherSerializer(instance.teacher_id).data

        return response
