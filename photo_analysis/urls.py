from django.urls import path
from .views import home, upload_image, gallery, delete_image  # Import your views

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_image, name='upload_image'),
    path('gallery/', gallery, name='gallery'),
    path('delete/<int:image_id>/', delete_image, name='delete_image')
]
