from django.db import models
from django.utils import timezone
from accounts.models import Teacher, User, Student


class ChatRoom(models.Model):
    teachers = models.ManyToManyField(Teacher)
    students = models.ManyToManyField(Student)
    last_message = models.CharField(max_length=255, null=True)
    last_message_time = models.DateTimeField(null=True)
    sender_id = models.UUIDField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    # @property
    # def name(self):
    #     teacher_names = ', '.join(teacher.full_name for teacher in self.teachers.all())
    #     student_names = ', '.join(student.full_name for student in self.students.all())
    #     teachers_part = f'{teacher_names}' if teacher_names else ''
    #     students_part = f'{student_names}' if student_names else ''
    #     return teachers_part + students_part


    @property
    def image(self):
        if self.students.exists():
            return self.students.first().image.url
        elif self.teachers.exists():
            return self.teachers.first().image.url
            
        return None
    
    # def update_name(self, new_name):
    #     self.name = new_name
    #     self.save()

    # def __str__(self):
    #     return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.content}'