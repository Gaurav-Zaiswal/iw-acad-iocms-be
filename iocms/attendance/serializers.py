from rest_framework import serializers
from users.serializers import StudentSerializer

from .models import AttendanceVideoModel


class AttendanceVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceVideoModel
        fields = ['video']
    
    # def to_representation(self, instance):
        # response = super().to_representation(instance)
        # response['user'] = StudentSerializer(instance.user).data
        # return response 
