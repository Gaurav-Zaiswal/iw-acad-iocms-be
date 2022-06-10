from django.db import models
from django.utils.timezone import now 
from classroom.models import Classroom , ClassroomStudents
from users.models import Student, Teacher 

#assignment post by teacher
class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    paper = models.FileField(upload_to='assignment/')
    points = models.IntegerField()
    creation_date = models.DateTimeField(default=now)
    deadline = models.DateTimeField()

    def __str__(self) -> str:
        return self.title[0:20]


#assignment submit by student
class AssignmentByStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE )
    assignment_details = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    assignment_answer = models.FileField(upload_to='assignments/', blank=True, null=True)
    assignment_link = models.URLField(blank=True, null = True)
    submisson_date = models.DateTimeField(default=now)
