from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CreateStudentView


router = DefaultRouter()
router.register('api/student-register', CreateStudentView, basename='StudentModel')


urlpatterns = [
    path('', include(router.urls)),
]

