import uuid
from django.db import models

class RFID(models.Model):
    rfid_number = models.CharField(max_length=50, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when an object is created

    # Add any additional fields related to RFID data if needed

    def __str__(self):
        return self.rfid_number
