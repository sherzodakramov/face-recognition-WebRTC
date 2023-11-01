from django.urls import path
from . import views
from .views import UserProfileAPIView

urlpatterns = [
    #path('', views.home, name=''),
    path('detect_faces', views.detect_faces, name='home'),
    # path('recognition/', views.detect_faces, name='recognition'),
    path('api/profiles/', UserProfileAPIView.as_view(), name='user-profiles'),
]
