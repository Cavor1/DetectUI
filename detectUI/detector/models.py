from django.db import models
from django.conf import settings

def image_path(instance,filename):
    return f'uploads/user_{instance.user.id}/{filename}'

class uploadedImage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="images"
    ) 
    image = models.ImageField(upload_to=image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
