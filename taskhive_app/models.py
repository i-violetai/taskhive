from django.db import models

# Create your models here.
from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    processed_image = models.ImageField(upload_to='processed_images/', null=True, blank=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Image {self.id}"
