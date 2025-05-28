from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'accept': 'image/jpeg,image/png,image/gif,image/webp',
                'class': 'file-input'
            })
        }
