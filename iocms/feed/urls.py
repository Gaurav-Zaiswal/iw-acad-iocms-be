from django.urls import path

from .views import ( FeedView,
                     FeedCreateView,
                     ClassroomFeedDetailView )

app_name = 'class'

urlpatterns = [

    path('api/', FeedView.as_view()),
    path('api/create/', FeedCreateView.as_view()),
    # path('api/list/', FeedListView.as_view()),
    path('api/detail/<int:pk>', ClassroomFeedDetailView.as_view()),
]