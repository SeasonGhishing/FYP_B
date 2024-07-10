# serializers.py

from rest_framework import serializers

from .models import Student, Teacher, OTP
from rest_framework import serializers
from django.contrib.auth import get_user_model


class StudentSerializer(serializers.ModelSerializer):
    assigned_class_name = serializers.ReadOnlyField(source='assigned_class.name')

    class Meta:
        model = Student
        fields = ['id', 'email', 'password', 'role', 'full_name', 'rfid_number', 'gender', 'phone_number', 'parent_name', 'image', 'assigned_class', 'assigned_class_name']

    def get_student_class_name(self, obj):
        if obj.student_class:
            return obj.student_class.name
        return None


class TeacherSerializer(serializers.ModelSerializer):
    assigned_class_name = serializers.ReadOnlyField(source='assigned_class.name')
    class Meta:
        model = Teacher
        fields = ['id','email', 'password','role', 'full_name', 'rfid_number', 'gender', 'phone_number', 'image', 'assigned_class', 'assigned_class_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'role')

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['user', 'otp_secret', 'created_at']
