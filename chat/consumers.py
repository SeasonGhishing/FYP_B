# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import User
from .models import ChatRoom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'
        # Authenticate the WebSocket connection with JWT token from headers
        try:
            authorization_header = next(
                (header for header in self.scope['headers'] if header[0] == b'authorization'), None)
            if authorization_header:
                jwt_token = authorization_header[1].decode("utf-8").split()[1]
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(jwt_token)
                user = await self.get_user(validated_token)
                self.scope['user'] = user
            else:
                print("else")
                raise AuthenticationFailed('Authorization header not found')
        except (AuthenticationFailed, IndexError):
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Get or create the room asynchronously
        room = await self.get_or_create_room(self.room_name)

        # Save the message to the database asynchronously and retrieve the message instance
        message = await self.save_message(room, message_content)

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': message_content,
                'id': message.id,
                'timestamp':str(message.timestamp),
                'sender_id':str(message.sender_id)
            }
        )

    async def chat_message(self, event):
        message = event['content']
        message_id = event['id'] 
        timestamp = event['timestamp']
        sender_id = event['sender_id']

        # Send message and message ID to WebSocket
        await self.send(text_data=json.dumps({
            'content': message,
            'id': message_id,
            'timestamp':timestamp,
            'sender':sender_id
        }))

    @database_sync_to_async
    def get_user(self, validated_token):
        user_id = validated_token['user_id']
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_or_create_room(self, room_name):
        room, _ = ChatRoom.objects.get_or_create(id=room_name)
        return room

    @database_sync_to_async
    def save_message(self, room, message_content):
        message = Message.objects.create(
            chat_room=room,
            sender=self.scope['user'],
            content=message_content
        )
        message.save()
        room.last_message = message.content
        room.last_message_time = message.timestamp
        room.sender_id = self.scope['user'].id
        room.save()
        return message
