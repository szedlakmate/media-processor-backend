from django.urls import path
from .views import *

urlpatterns = [
    path('', upload_file, name='upload_file'),
    path('package_content', package_content, name='package_content')
]
