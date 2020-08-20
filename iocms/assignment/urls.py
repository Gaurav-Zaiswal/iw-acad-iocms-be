from django.urls import path 
from .views import AssignmentView, AssignmentSubmitView, AssignmentDetailView
app_name = 'assignment'

urlpatterns = [
    path('list', AssignmentView.as_view(), name = 'list'),
    path('list/<int:pk>/', AssignmentDetailView.as_view(), name = 'details'),
    path('submit/', AssignmentSubmitView.as_view(), name = 'submit')
] 