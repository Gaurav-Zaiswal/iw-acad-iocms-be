from django.urls import path 
from .views import (
                    AssignmentListView,
                    AssignmentCreateView, 
                    AssignmentSubmitView, 
                    AssignmentDetailView )
app_name = 'assignment'

urlpatterns = [
    path('list', AssignmentListView.as_view(), name = 'list'),
    path('create', AssignmentCreateView.as_view(), name = 'create'),
    path('list/<int:pk>/', AssignmentDetailView.as_view(), name = 'details'),
    path('list/<int:pk>/submit/', AssignmentSubmitView.as_view(), name = 'submit')
] 