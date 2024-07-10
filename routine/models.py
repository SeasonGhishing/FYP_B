from django.db import models
from classes.models import Class
from accounts.models import Teacher

class Routine(models.Model):
    DAYS_OF_WEEK_CHOICES = (
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Entire Week', 'For Entire Week'),
    )
    subject = models.CharField(max_length=100)
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    target_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    day_of_week = models.CharField(max_length=50, choices=DAYS_OF_WEEK_CHOICES, blank=True, null=True)

    def __str__(self):
        if self.assigned_teacher: 
            return f"{self.subject} - {self.assigned_teacher}"
        else:
            return f"{self.subject} - No Teacher Assigned"

    def save(self, *args, **kwargs):
        if self.start_time:
            self.start_time = self.start_time.replace(second=0, microsecond=0)
        if self.end_time:
            self.end_time = self.end_time.replace(second=0, microsecond=0)

        super().save(*args, **kwargs)