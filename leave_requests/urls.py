# urls.py

from django.urls import path
from .views import LeaveRequestAPIView, LeaveRequestAllView, LeaveRequestDetailView

urlpatterns = [
    path('', LeaveRequestAPIView.as_view(), name='leave-request'),
    path('all/', LeaveRequestAllView.as_view(), name='leave-request'),
    path('<int:pk>/', LeaveRequestDetailView.as_view(), name='leave-request'),
]
