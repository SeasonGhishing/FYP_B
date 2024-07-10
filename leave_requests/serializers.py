from rest_framework import serializers
from accounts.serializers import StudentSerializer, TeacherSerializer
from .models import LeaveRequest

class LeaveRequestSerializer(serializers.ModelSerializer):
    requester_details = serializers.SerializerMethodField()
    name = serializers.ReadOnlyField(source='requester.name')
    role = serializers.ReadOnlyField(source='requester.role')

    class Meta:
        model = LeaveRequest
        fields = ['id', 'requester', 'requester_details', 'reason', 'description', 'status', 'created_at', 'name', 'role']

    def get_requester_details(self, obj):
        user = obj.requester
        if hasattr(user, 'teacher'):
            serializer = TeacherSerializer(user.teacher)
        elif hasattr(user, 'student'):
            serializer = StudentSerializer(user.student)
        else:
            serializer = None
        return serializer.data if serializer else {}
