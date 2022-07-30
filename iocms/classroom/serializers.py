from rest_framework import serializers
from rest_framework import response

from .models import Classroom, ClassroomStudents, Rating
from users.serializers import UserSerializer, TeacherSerializer, StudentSerializer


class BasicClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id']


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
        response['enrolled_student_id'] = StudentSerializer(instance.enrolled_student_id).data # add foreign key
        return response 

class RatingSerializer(serializers.ModelSerializer):
    """
    serializer class to for rating.
    """
    class Meta:
        model = Rating
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['rated_by'] = StudentSerializer(instance.rated_by).data # add foreign key
        response['classroom_id'] = BasicClassroomSerializer(instance.classroom).data # add foreign key
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


class ClassroomListElasticSerializer(serializers.ModelSerializer):
    """
    serializer for elastic search to list search results
    """
    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'class_description'] 

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['created_by'] = TeacherSerializer(instance.created_by).data
    #     return response 


class RecommendationListSerializer(serializers.Serializer):
    """
    serializer for recommendation objects.
    """
    classroom_id = serializers.IntegerField()
    classroom_description = serializers.CharField(max_length=500, required=False)
    classroom_name = serializers.CharField(max_length=150)


class ClassroomSearchSerializer(serializers.ModelSerializer):
    """
    serializer for basic django search functionality
    """
    class Meta:
        model = Classroom
        fields = ['id', 'class_name', 'class_description', 'class_code'] 

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['created_by'] = TeacherSerializer(instance.created_by).data
    #     return response 