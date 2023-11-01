from django.contrib import admin
from .models import UserProfile, FaceRecognitionResult

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FaceRecognitionResult)