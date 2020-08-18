import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):
    # adding custom field
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # now user can log in using email
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # here, email is already a required field

    def __str__(self):
        return self.username


class Student(models.Model):
    # adding custom field
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Teacher(models.Model):
    # adding custom field
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
