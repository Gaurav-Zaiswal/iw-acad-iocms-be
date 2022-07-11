from django.urls import path

from .views import ( FeedView,
                     FeedCreateView,
                     FeedListView,
                     ClassroomFeedDetailView )
# from rest_framework.routers import DefaultRouter


app_name = 'class'

# router = DefaultRouter()
# router.register('api/list', FeedListView, basename='ClassroomFeedModel')

urlpatterns = [

    path('api/', FeedView.as_view()),
    path('api/<int:class_id>/create/', FeedCreateView.as_view()),
    path('api/<int:class_id>/list/', FeedListView.as_view()),
    path('api/detail/<int:pk>/', ClassroomFeedDetailView.as_view()),
]

# urlpatterns += router.urls
