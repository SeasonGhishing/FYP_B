from rest_framework import serializers

from accounts.serializers import StudentSerializer, TeacherSerializer
from .models import ChatRoom, Message

class ChatRoomSerializer(serializers.ModelSerializer):
    # name = serializers.ReadOnlyField()
    # image = serializers.ReadOnlyField()
    teachers = TeacherSerializer(many=True)
    students = StudentSerializer(many=True)

    class Meta:
        model = ChatRoom
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = '__all__'
