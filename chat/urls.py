from django.urls import path 
from . import views 
from .views import MessageListAPIView, MessageDetailAPIView, RoomMessageAPIView

urlpatterns = [
    # path('', views.lobby),
    path('', views.chat_room, name='chat-room'),
    path('chatrooms/', views.ChatRoomListAPIView.as_view(), name='chatroom-list'),
    path('chatrooms/<int:pk>/', views.ChatRoomDetailAPIView.as_view(), name='chatroom-detail'),
    path('my_room/', views.MyRoomDetailApiView.as_view(), name='get-room'),
    path('messages/', MessageListAPIView.as_view(), name='message-list'),
    path('messages/<int:room_id>/', RoomMessageAPIView.as_view(), name='message-list-of-room'),

    path('messages/<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),
]