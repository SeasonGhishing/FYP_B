import datetime
from django.db import models
from classes.models import Class

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    target_class = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
