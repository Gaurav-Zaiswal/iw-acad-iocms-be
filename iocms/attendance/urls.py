from django.urls import path

from .views import UploadAttendanceVideo

app_name = 'attendance'

urlpatterns = [
    path('api/upload-video/', UploadAttendanceVideo.as_view())
]