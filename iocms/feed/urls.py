from django.urls import path

from .views import FeedCreateView

app_name = 'class'

urlpatterns = [

    # path('api/', ClassroomView.as_view()),
    path('api/create/', FeedCreateView.as_view()),
    # path('api/list/', ClassroomFeedListView.as_view()),
    # path('api/detail/<int:pk>', ClassroomFeedDetailView.as_view()),
]