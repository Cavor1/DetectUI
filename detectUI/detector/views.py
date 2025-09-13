from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import UploadedImage, Detection
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm
from .services.registry import inference_models
from PIL import Image


def addDetection(image : UploadedImage,inference_model : str , labels):
    Detection.objects.update_or_create(
        image = image,
        inference_model = inference_model,
        defaults={
            "detections" : labels,
        }
    )



@login_required
def main(request):

    form = ImageUploadForm()
    labels = None



    images = (
        UploadedImage.objects
        .filter(user=request.user)
    )
    selected_id = request.GET.get('img')
    selected_model = request.GET.get('model')
    selected_img = UploadedImage.objects.filter(pk=selected_id,user=request.user).first()
    detection = Detection.objects.filter(image = selected_img, inference_model = selected_model).first()
    if detection is not None:
        detections = detection.detections
    else:
        detections = None
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
                result = inference_models[model].detect(img)
                labels = result.labels
                addDetection(selected_img,model,labels)

            except Exception as e:
                labels = [f'{e}']


            return HttpResponseRedirect(f'/?img={selected_id}&model={selected_model}')



    return render(request, 'detector/main.html',{
        'images':images,
        'form':form,
        'selected':selected_img,
        'selected_model':selected_model,
        'model_list':list(inference_models.keys()),
        'labels': detections
    })
# Create your views here.
