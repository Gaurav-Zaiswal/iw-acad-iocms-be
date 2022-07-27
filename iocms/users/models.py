import uuid
# import Pillow

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model
#
# User = get_user_model()


def covert_to_grayscale(file):
    # TODO
    # convert given image to grayscale and return it
    pass


def profile_pic_path(instance, filename):
    # checks jpg exttension

    extension = filename.split('.')[1]
    if len(filename.split('.')) != 2:
        raise ValidationError("image seems currupted...")
    if extension not in ['jpg', 'jpeg']:
        raise ValidationError("we currently accept jpg/jpeg formats only.")
    unique_name = uuid.uuid4().hex
    # print('author_pictures/' + unique_name + '.' + extension)
    return 'author_pictures/' + unique_name + '.' + extension



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


class Profile(models.Model):
    image = models.ImageField(upload_to=profile_pic_path)