from django.urls import path
from .views import VoiceboxAPIView
from .views import StardogGetLastUpdatedAPIView

urlpatterns = [
    path('voicebox-data/', VoiceboxAPIView.as_view(), name='voicebox-data'),
    path('stardog-last-updated/', StardogGetLastUpdatedAPIView.as_view(), name='stardog-last-updated'),
]