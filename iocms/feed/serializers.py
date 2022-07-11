from rest_framework import serializers
from rest_framework import response

from .models import ClassroomFeed
from users.serializers import UserSerializer, TeacherSerializer, StudentSerializer
from assignment.serializers import AssignmentDetailSerializer


class ClassroomFeedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomFeed
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['posted_by'] = TeacherSerializer(instance.posted_by).data

        return response


class ClassroomFeedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomFeed
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['posted_by'] = TeacherSerializer(instance.posted_by).data
        response['assignment_id'] = AssignmentDetailSerializer(instance.assignment_id).data
        return response


class ClassroomFeedDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassroomFeed
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['posted_by'] = TeacherSerializer(instance.posted_by).data
        return response
