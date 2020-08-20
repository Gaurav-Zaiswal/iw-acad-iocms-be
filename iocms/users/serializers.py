from .models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator  # makes sure email, username are unique

from .models import Student


class StudentRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(
        max_length=150
    )
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        min_length=8,
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            is_student = True
        )
        password = self.validated_data['password']
        user.set_password(password)
        #
        user.save()
        #
        student = Student(user=user)
        student.save()

        return user



