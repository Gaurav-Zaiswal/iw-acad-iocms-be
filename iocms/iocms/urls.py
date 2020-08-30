from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('class/', include('classroom.urls')),
    path('users/', include('users.urls'), name="user-register")
]
