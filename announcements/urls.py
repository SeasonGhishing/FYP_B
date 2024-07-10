# announcements/urls.py
from django.urls import path
from .views import AnnouncementAPIView, AnnouncementDetailAPIView

app_name = 'announcements'

urlpatterns = [
    path('announcement-list', AnnouncementAPIView.as_view(), name='announcement-list'),
    path('<int:pk>/', AnnouncementDetailAPIView.as_view(), name='announcement-detail'),
]
