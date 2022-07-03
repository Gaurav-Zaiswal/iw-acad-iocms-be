from rest_framework import serializers
from rest_framework import response

from .models import Classroom, ClassroomStudents, Rating
from users.serializers import UserSerializer, TeacherSerializer, StudentSerializer


class ClassroomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'class_description', 'created_by']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['created_by'] = TeacherSerializer(instance.created_by).data
        return response

    
class ClassroomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"

    def to_representation(self, instance):
        """
        add additional data to serializer
        """
        representation = super().to_representation(instance)
        representation['created_by'] = TeacherSerializer(instance.created_by).data   # add teacher's details
        representation['no_of_ratings'] = self.context['no_of_ratings']  # add data that come via context from view
        representation['avg_rating'] = self.context['avg_rating']
        return representation


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



class TopRatedClassSerializer(serializers.Serializer):
    """
    Serialize Top Rating Classrooms, but give different key names than that are defined in queryset.
    e.g. queryset have classroom__id defined but we want class_id in API response.
    """

    class_id = serializers.IntegerField(source='classroom__id')
    class_name = serializers.CharField(source='classroom__class_name')
    class_description = serializers.CharField(source='classroom__class_description')
    instructor_id = serializers.IntegerField(source='classroom__created_by')
    avg_rating = serializers.FloatField()  # keep 'avg_rating' same
