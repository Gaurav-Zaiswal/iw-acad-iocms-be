from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField 
from .models import Teacher, Student, Assignment, AssignmentByStudent




class AssignmentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = [ 'teacher', 'title', 'description','points', 'deadline']

   

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


