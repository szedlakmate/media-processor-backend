from django.urls import path

from .views import *

urlpatterns = [
    path('', upload_file, name='upload_file'),
    path('packaged_content', packaged_content, name='packaged_content'),
    path('packaged_content/<int:packaged_content_id>', packaged_content_status, name='packaged_content_status'),
]
