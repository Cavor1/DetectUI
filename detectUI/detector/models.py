from typing import Mapping
from django.db import models
from django.conf import settings
from django.utils import timezone
def image_path(instance,filename):
    return f'uploads/user_{instance.user.id}/{filename}'

class UploadedImage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="images"
    ) 
    image = models.ImageField(upload_to=image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    image = models.ForeignKey(
        UploadedImage,
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-modified_at"]


class Message(models.Model):
    ROLE_CHOICES = {
        'user':'user',
        'assistant':'assistant'
    }
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role= models.CharField(max_length=10, choices=ROLE_CHOICES)

