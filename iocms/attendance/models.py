import uuid

from django.db import models
from django.core.exceptions import ValidationError

from users.models import Student

def video_renaming(instance, filename):
    extension = filename.split('.')[1]
    if len(filename.split('.')) != 2:
        raise ValidationError("Video seems corrupted...")
    if extension not in ['mp4', 'MP4', 'WEBM', 'MKV']:
        raise ValidationError("we currently accept mp4, webm, and mkv formats only.")
    unique_name = uuid.uuid4().hex[:8]
    # print('author_pictures/' + unique_name + '.' + extension)
    return 'attendance_video/' + unique_name + '.' + extension

# Create your models here.
class AttendanceVideoModel(models.Model):
    # user = models.ForeignKey(Student, related_name="user_id", on_delete=models.CASCADE)
    video = models.FileField(upload_to=video_renaming)
