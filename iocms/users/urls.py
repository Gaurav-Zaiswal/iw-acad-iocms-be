from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views

from .views import (
    CreateStudentView, CreateTeacherView, UserLogoutView, UserView, UploadImage
)


app_name = "users"

router = DefaultRouter()
router.register('api/student-register', CreateStudentView, basename='StudentModel')
router.register('api/teacher-register', CreateTeacherView, basename='TeacherModel')
# router.register('api/user-info', UserView, basename = 'UserModel')


urlpatterns = [
    path('', include(router.urls)),
    path('api/profile/upload-image/', UploadImage.as_view(), name='upload-imgage'),
    path('api/login/', auth_views.obtain_auth_token, name='login'),
    path('api/user-info/', UserView.as_view(), name = 'user-info'),
    path('api/logout/', UserLogoutView.as_view(), name = "user-logout") 
]
 
