from rest_framework import serializers

from .models import Student, Teacher


class StudentRegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = Student
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password' : {'write_only': True}
        }

        def save(self):
            student = Student(
                username=self.validated_data['username'],
                email=self.validated_data['email'],
            )
            password = self.validated_data['password']
            confirm_password = self.validated_data['confirm_password']

            if password != confirm_password:
                raise serializers.ValidationError(
                    {'password': 'Password did not match!'}
                )

            student.set_password(password)

            student.save()
            return student
