from django.contrib import admin

from .models import Classroom, Rating

# Register your models here.
admin.site.register([Classroom, Rating])