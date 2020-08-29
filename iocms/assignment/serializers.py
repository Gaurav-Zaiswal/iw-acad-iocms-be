from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import HyperlinkedIdentityField 
from users.models import Teacher, Student
from .models import  Assignment, AssignmentByStudent




class AssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'points', 'deadline','teacher']


class AssignmentListSerializer(serializers.HyperlinkedModelSerializer):
    details = HyperlinkedIdentityField(lookup_field = 'pk', view_name='assignment:details')
    class Meta:
        model = Assignment
        fields = ['id', 'details']


class AssignmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class AssignmentSubmitSerializer(serializers.ModelSerializer): 
    assignment_link = serializers.URLField()

    class Meta:
        model = AssignmentByStudent
        fields = ['student','assignment_details','assignment_link', 'assignment_answer']


