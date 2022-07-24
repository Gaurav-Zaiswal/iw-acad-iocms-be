from django.urls import path 

from .views import SearchClassroom

urlpatterns = [
    path('<str:query>/', SearchClassroom.as_view())
]
