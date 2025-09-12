from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UploadedImage
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm
from .services.registry import inference_models
from PIL import Image


@login_required
def main(request):

    form = ImageUploadForm()
    labels = None



    images = (
        UploadedImage.objects
        .filter(user=request.user)
    )
    selected_id = request.GET.get('img')
    selected_img = UploadedImage.objects.filter(pk=selected_id,user=request.user).first()


    if request.method == 'POST':

        form_name = request.POST.get('form_name')
        if form_name == 'form_upload':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                img = form.save(commit=False)
                img.user = request.user
                img.save()
                return redirect('main')
        if form_name == 'form_detect' and selected_img is not None:
            model = request.POST.get('model')
            try:
                img = Image.open(selected_img.image.path)
                result = inference_models[model].detect(img)  # your InferenceResult
                labels = result.labels
                labels = labels
            except Exception as e:
                labels = [f'{e}']





    return render(request, 'detector/main.html',{
        'images':images,
        'form':form,
        'selected':selected_img,
        'model_list':inference_models,
        'labels': labels
    })
# Create your views here.
