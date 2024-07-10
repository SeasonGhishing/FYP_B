from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accounts.models import User
from .models import ChatRoom
from .serializers import ChatRoomSerializer
from .models import Message
from .serializers import MessageSerializer
from django.shortcuts import render
from django.shortcuts import get_object_or_404
import jwt

def chat_room(request):
    room_name = 'test'  # You need to determine how to get the room name dynamically
    return render(request, 'chat/chat_room.html', {'room_name': room_name})


class ChatRoomListAPIView(APIView):
    def get(self, request):
        chat_rooms = ChatRoom.objects.all()

        serializer = ChatRoomSerializer(chat_rooms, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = ChatRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatRoomDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return ChatRoom.objects.get(pk=pk)
        except ChatRoom.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        chat_room = self.get_object(pk)
        serializer = ChatRoomSerializer(chat_room)
        return Response(serializer.data)
    
    def patch(self, request, pk):  # Changed from put to patch
        chat_room = self.get_object(pk)
        serializer = ChatRoomSerializer(chat_room, data=request.data, partial=True)  # Using partial=True for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        chat_room = self.get_object(pk)
        chat_room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageListAPIView(APIView):
    def get(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
 
    def post(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]  # Assuming the token is in the format "Bearer <token>"

        # Decode the token to get user ID
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            user_id = decoded_token.get('user_id')
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNzM2NDQ2LCJpYXQiOjE3MTI3MzU1NDYsImp0aSI6IjcyZjlkMWJhZGQ2NTQwZGE5NjIyMDgyNTFhOTViYTMzIiwidXNlcl9pZCI6ImQ2NTE0OWY5LWU4OTYtNGQ4MS1iMjYzLTE4OTZkNWU2MjczNSJ9.ony1RzoN-ivRZCJxtJ9Tdttyq-KwARNNf_wvI_BCccE"
        user = get_object_or_404(User, id=user_id)
        
        # Validate chat room ID and retrieve chat room
        chat_room_id = request.data.get('chat_room')
        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)

        # Create message object
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['sender_id'] = user.id
            serializer.validated_data['chat_room_id'] = chat_room_id
            message = serializer.save()

            # Update last message details in the chat room
            chat_room.last_message = message.content
            chat_room.last_message_time = message.timestamp
            chat_room.sender_id = user.id
            chat_room.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404
# api/chat/get-message/73
    def get(self, request, pk):
        message = self.get_object(pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def delete(self, request, pk):
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RoomMessageAPIView(APIView):
    def get(self, request, room_id):
        # Get chat room
        messages = Message.objects.filter(chat_room__id=room_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class MyRoomDetailApiView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]

        # Decode the token to get user ID
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            user_id = decoded_token.get('user_id')
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = get_object_or_404(User, id=user_id)
        if user.role == "Student":
            
        # Filter ChatRoom instances where the user is present
            chat_rooms = ChatRoom.objects.filter(students=user).distinct()
        
        else:
            chat_rooms = ChatRoom.objects.filter(teachers=user).distinct()
            

        # Serialize the queryset of ChatRoom objects
        serializer = ChatRoomSerializer(chat_rooms, many=True)
        
        # Return the serialized data in the response
        return Response(serializer.data)