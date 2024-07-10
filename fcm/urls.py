from django.urls import path
from .views import FCMTokenView

urlpatterns = [
    path('', FCMTokenView.as_view(), name='store_fcm_token'),
]