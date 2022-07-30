from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from search.views import RecomendationView

from classroom.views import Lookup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('class/', include('classroom.urls')),
    path('assignment-api/', include('assignment.urls', namespace='assignment')),
    path('feed/', include('feed.urls', namespace='feed')),
    path('users/', include('users.urls'), name="user-register"),
    path('attendance/', include('attendance.urls'), name="user-attendance"),
    path('search/', include('search.urls'), name='search'), # requires elasticsearch
    path('lookup/<str:q>/', Lookup.as_view(), name='normal-search'),
    path('for-you/', RecomendationView.as_view(), name='for-you'),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
