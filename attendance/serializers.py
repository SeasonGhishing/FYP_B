from rest_framework import serializers
from accounts.serializers import StudentSerializer, TeacherSerializer
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ['id', 'user', 'user_details', 'date', 'entry_time', 'exit_time', 'status']

    def get_user_details(self, obj):
        user = obj.user
        if hasattr(user, 'teacher'):
            serializer = TeacherSerializer(user.teacher)
        elif hasattr(user, 'student'):
            serializer = StudentSerializer(user.student)
        else:
            serializer = None
        return serializer.data if serializer else {}
