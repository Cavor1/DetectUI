from django.shortcuts import render
from django.http import HttpResponse
from .models import UploadedImage

def main(request):
    images = (
        UploadedImage.objects
        .filter(user=request.user)
    ) 
    return render(request, 'detector/main.html',{'images':images})
# Create your views here.
