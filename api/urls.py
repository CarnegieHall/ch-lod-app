from django.urls import path
from .views import VoiceboxAPIView

urlpatterns = [
    path('voicebox-data/', VoiceboxAPIView.as_view(), name='voicebox-data'),
]