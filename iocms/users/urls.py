from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CreateStudentView, CreateTeacherView


router = DefaultRouter()
router.register('api/student-register', CreateStudentView, basename='StudentModel')
router.register('api/teacher-register', CreateTeacherView, basename='TeacherModel')


urlpatterns = [
    path('', include(router.urls)),
]

