from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('photo_analysis.urls')),
]

# Add error handlers
handler404 = 'photo_analysis.views.handler404'
handler500 = 'photo_analysis.views.handler500'

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
