from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('class/', include('class.urls')),
    path('users/', include('users.urls'), name="user-register"),
    path('assignment-api/', include('assignment.urls', namespace='assignment'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
