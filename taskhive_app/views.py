from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ImageUploadForm
from .tasks import full_image_processing_pipeline
from .models import UploadedImage

# Create your views here.

def image_upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            # Trigger the Celery task to process the image
            full_image_processing_pipeline.apply_async(args=[uploaded_image.id])
            print(uploaded_image.processed_image)
            return redirect('image_detail', image_id=uploaded_image.id)
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

def image_detail_view(request, image_id):
    uploaded_image = UploadedImage.objects.get(id=image_id)
    return render(request, 'image_detail.html', {'image': uploaded_image})
