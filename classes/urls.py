from django.urls import path
from .views import ClassListCreateAPIView, ClassRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', ClassListCreateAPIView.as_view(), name='class-list-create'),
    path('<int:pk>/', ClassRetrieveUpdateDestroyAPIView.as_view(), name='class-detail'),
]
