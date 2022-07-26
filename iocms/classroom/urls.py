from django.urls import path

from .views import ClassroomView, ClassroomDetailView, ClassroomCreateView, \
    ClassroomListView, ClassroomAddView, TopRatedClassrooms, RateClassroom

app_name = 'class'

urlpatterns = [
    path('api/', ClassroomView.as_view()),
    path('api/create/', ClassroomCreateView.as_view()),
    path('api/list/', ClassroomListView.as_view()),
    path('api/detail/<int:pk>', ClassroomDetailView.as_view()),
    path('api/join/', ClassroomAddView.as_view()),
    path('api/rate/<int:pk>/', RateClassroom.as_view()),
    path('api/top-rated-classes/', TopRatedClassrooms.as_view())
]