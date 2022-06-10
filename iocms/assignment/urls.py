from django.urls import path 
from .views import (
                    AssignmentListView,
                    AssignmentCreateView, 
                    AssignmentSubmitView, 
                    AssignmentDetailView,
                    SubbmittedAssignmentView)
app_name = 'assignment'

urlpatterns = [

    path('class/<int:class_pk>/list', AssignmentListView.as_view(), name = 'list'),
    path('class/<int:class_pk>/create/', AssignmentCreateView.as_view(), name = 'create'),
    path('class/list/<int:pk>', AssignmentDetailView.as_view(), name = 'details'),
    path('<int:pk>/submit', AssignmentSubmitView.as_view(), name = 'submit'),
    path('<int:class_pk>/submitted-assignment-list', SubbmittedAssignmentView.as_view(), name='submitted-list')
]
