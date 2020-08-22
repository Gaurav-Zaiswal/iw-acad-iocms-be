from django.contrib import admin

# Register your models here.
from .models import Assignment, AssignmentByStudent

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'creation_date', 'deadline')

    class Mets:
        model = Assignment

@admin.register(AssignmentByStudent)
class AssignmentAdmin(admin.ModelAdmin):
    
    list_display = ( 'student','submisson_date')

    class Meta:
        model = AssignmentByStudent
