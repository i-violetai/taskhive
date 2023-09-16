from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.image_upload_view, name='image_upload'),
    path('image/<int:image_id>/', views.image_detail_view, name='image_detail'),
]
