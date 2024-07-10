# from django.urls import re_path 
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
# ]

from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
