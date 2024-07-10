from django.urls import path
from .views import NotificationListAPIView, NotificationDetailAPIView, NotificationSpecificAPIView

urlpatterns = [
    path('all/', NotificationListAPIView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetailAPIView.as_view(), name='notification-detail'),
    path('', NotificationSpecificAPIView.as_view(), name='notification-detail'),
]
