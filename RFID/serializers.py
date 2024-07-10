from rest_framework import serializers
from .models import RFID

class RFIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFID
        fields = ['rfid_number', 'created_at']
