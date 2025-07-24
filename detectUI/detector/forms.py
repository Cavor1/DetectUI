from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={
                "class": "block w-full text-sm text-gray-600",
            })
        }


