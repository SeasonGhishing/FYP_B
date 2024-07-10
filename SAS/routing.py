# project_name/routing.py
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    # Other URL patterns
    path('chat/', include('chat.routing')),
]
