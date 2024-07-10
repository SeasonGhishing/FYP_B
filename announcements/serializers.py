# serializers.py
from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    target_class_name = serializers.ReadOnlyField(source='target_class.name')
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'timestamp', 'target_class','target_class_name']
