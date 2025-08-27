from django import forms
from django.db.models import Model
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

class ModelsFrom(forms.Form):
    field = forms.ChoiceField()
