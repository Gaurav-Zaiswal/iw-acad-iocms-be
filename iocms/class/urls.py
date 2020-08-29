from django.urls import path

from .views import ClassroomView, ClassroomDetailView, ClassroomCreateView, ClassroomListView, ClassroomAddView

app_name = 'class'

urlpatterns = [
    path('', ClassroomView.as_view()),
    path('create/', ClassroomCreateView.as_view()),
    path('list/', ClassroomListView.as_view()),
    path('detail/<int:pk>', ClassroomDetailView.as_view()),
    path('join/', ClassroomAddView.as_view())
]