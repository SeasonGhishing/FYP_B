from django.contrib.auth.models import User
from django.db import models

from SAS import settings

class FCMToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        return f'FCM Token for {self.user.username}'
