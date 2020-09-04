from django.db import models
from users.models import Teacher
from assignment.models import Assignment
from classroom.models import Classroom


class ClassroomFeed(models.Model):
    classroom_id = models.ManyToManyField(Classroom, blank=True)
    assignment_id = models.OneToOneField(Assignment, on_delete=models.CASCADE, blank=True)
    posted_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    assignment_title = models.CharField(max_length=150)
    assignment_description = models.CharField(max_length=500)

    def __str__(self):
        return f"Feed of {self.classroom_id.class_name} posted by {self.teacher_id.username}"

