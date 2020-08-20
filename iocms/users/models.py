import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.contrib.auth import get_user_model
#
# User = get_user_model()


class User(AbstractUser):
    # adding custom field
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # now user can log in using email
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # here, email is already a required field

    def __str__(self):
        return self.username


class Student(models.Model):
    # adding custom field
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    # adding custom field
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username
