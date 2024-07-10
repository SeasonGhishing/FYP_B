from django.urls import path
from .views import RFIDAPIView

urlpatterns = [
    path('', RFIDAPIView.as_view(), name='rfid-list'),
]
