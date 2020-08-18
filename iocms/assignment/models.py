from django.db import models
from django.utils.timezone import now 





# Create your models here.
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.full_name



class Student(models.Model):
    id = models.AutoField(primary_key=True)
    # class_details = models.ManyToManyField(Class) 
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    
    def __str__(self):
        return self.full_name



#assignment post by teacher
class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    # class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank = True, null = True)
    points = models.IntegerField()
    creation_date = models.DateTimeField(default=now)
    deadline = models.DateTimeField()

    def __str__(self) -> str:
        return self.title[0:10]
    


#assignment submit by student
class AssignmentByStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE )
    assignment_details = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    assignment_answer = models.FileField(upload_to='assignments/', blank=True, null=True)
    assignment_link = models.URLField(blank=True, null = True)
    submisson_date = models.DateTimeField(default=now)





    
