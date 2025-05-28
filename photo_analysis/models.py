from django.db import models

# Create your models here
class UploadedImage(models.Model):
    image = models.ImageField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Image {self.id}"