from django.urls import path
from .views import RoutineApiView, RoutineListCreateAPIView, RoutineRetrieveUpdateDestroyAPIView

app_name = 'routine'

urlpatterns = [
    path('routine-list-create/', RoutineListCreateAPIView.as_view(), name='routine-list-create'),
    path('', RoutineApiView.as_view(), name='routines'),
    path('<int:pk>/', RoutineRetrieveUpdateDestroyAPIView.as_view(), name='routine-detail'),
]
