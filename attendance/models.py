# models.py

import datetime
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from nepali_datetime import date as NepaliDate

def get_current_nepali_date():
    return str(NepaliDate.today().isoformat())

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attendances', on_delete=models.CASCADE)
    date = models.DateField(default=get_current_nepali_date)
    entry_time = models.TimeField(blank=True, null=True)
    exit_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default='-')

