from django.db import models
import uuid

class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    teacher_id = models.UUIDField(blank=True, null=True)

    def assign_teacher(self, teacher_id):
        self.teacher_id = teacher_id
        self.save()
