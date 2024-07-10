# urls.py

from django.urls import path
from .views import AbsentView, AttendanceDetailView, AttendanceSpecificAPIView, AttendanceTodayView, AttendanceView, AttendanceAllView, InformedApiView

urlpatterns = [
    path('', AttendanceView.as_view(), name='attendance-create'),
    path('absent/', AbsentView.as_view(), name='absent-create'),
    path('informed/', InformedApiView.as_view(), name='informed-create'),
    path('all/', AttendanceAllView.as_view(), name='attendance-all-detail'),
    path('specific/', AttendanceSpecificAPIView.as_view(), name='attendance-all-detail'),
    path('<int:pk>/', AttendanceDetailView.as_view(), name='attendance-detail'),
    path('today/', AttendanceTodayView.as_view(), name='attendance-today'),
]
