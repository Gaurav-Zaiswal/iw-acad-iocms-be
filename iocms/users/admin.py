
from django.contrib import admin
from .models import User, Teacher, Student
# Register your models here.



@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['email','is_superuser', 'is_teacher', 'is_student']
    
    class Meta:
        model = User
        


admin.site.register([Teacher, Student])

 