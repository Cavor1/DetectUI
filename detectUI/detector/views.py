from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UploadedImage
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm

model_list = ['a','b','c']


@login_required
def main(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.user = request.user
            img.save()
            return redirect('main')
    else:
        form = ImageUploadForm()
    images = (
        UploadedImage.objects
        .filter(user=request.user)
    )
    selected_id = request.GET.get("img")
    selected_img = UploadedImage.objects.filter(pk=selected_id,user=request.user).first()
    return render(request, 'detector/main.html',{'images':images, 'form':form, 'selected':selected_img, "model_list":model_list })
# Create your views here.
