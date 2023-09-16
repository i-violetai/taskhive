from celery import shared_task, chain
from PIL import Image, ImageFilter
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from .models import UploadedImage
from celery.exceptions import Retry
import os
from django.conf import settings



@shared_task
def full_image_processing_pipeline(image_id):
    chain(
        process_image_task.s(image_id),
        blur_image_task.s()
    ).apply_async()


@shared_task(bind=True)
def process_image_task(self, image_id):
    try:
        uploaded_image = UploadedImage.objects.get(id=image_id)
        image_path = uploaded_image.image.path

        with Image.open(image_path) as img:
            greyscale_image = img.convert('L')

            # Save the processed image to a BytesIO buffer
            buffer = BytesIO()
            greyscale_image.save(buffer, format='JPEG')
            buffer.seek(0)

            fs = FileSystemStorage()
            processed_image_path = fs.save(f'processed_images/{uploaded_image.id}_greyscale.jpg', buffer)

            # Update the image record in the database with the processed image (relative path)
            uploaded_image.processed_image = processed_image_path
            uploaded_image.is_processed = True
            uploaded_image.save()
            return image_id
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)


@shared_task(bind=True)
def blur_image_task(self, image_id):
    try:
        uploaded_image = UploadedImage.objects.get(id=image_id)

        # Use the relative path from the database
        image_path = os.path.join(settings.MEDIA_ROOT, uploaded_image.processed_image.name)

        with Image.open(image_path) as img:
            # Apply a blur filter
            blurred_image = img.filter(ImageFilter.GaussianBlur(radius=5))

            # Save the blurred image to a BytesIO buffer
            buffer = BytesIO()
            blurred_image.save(buffer, format='JPEG')
            buffer.seek(0)

            fs = FileSystemStorage()
            blurred_image_path = fs.save(f'processed_images/{uploaded_image.id}_blurred.jpg', buffer)

            # Update the image record in the database with the blurred image (relative path)
            uploaded_image.processed_image = blurred_image_path
            uploaded_image.is_processed = True
            uploaded_image.save()

        return 'Image blurred and saved.'
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)
