from django.db import models
from django.utils.timezone import now
from users.models import Teacher, Student
import random, string


class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=150)
    class_description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=now)
    is_class_code_enabled = models.BooleanField(default=True)
    class_code = models.CharField(max_length=8)
    def __str__(self):
        return self.class_name[0:10]

    def save(self, *args, **kwargs):
        self.class_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        super(Classroom, self).save(*args, **kwargs)

    class Meta:
        ordering = ['creation_date']


class ClassroomStudents(models.Model):
    classroom_id = models.OneToOneField(Classroom, on_delete=models.CASCADE)
    enrolled_student_id = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return self.classroom_id.class_name[0:10]
