from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password
import uuid
from django.http import HttpResponse
from django.utils import timezone
import pyotp
from django.db import models
from django.utils.crypto import get_random_string
from classes.models import Class

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'Admin', 'admin'
        STUDENT = 'Student', 'student'
        TEACHER = 'Teacher', 'teacher'
    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)
    # Common fields for all roles
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique = True, )
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Student(User):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    rfid_number = models.CharField(max_length=20, blank=True, null=True ,unique=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    parent_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='student_images/', null=True, blank=True)
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.role = User.Role.STUDENT

        # Update the User fields directly
        self.full_name = self.full_name
        self.rfid_number = self.rfid_number
        self.gender = self.gender
        self.phone_number = self.phone_number
        self.parent_name = self.parent_name
        self.assigned_class = self.assigned_class

        if self.password:
            self.password = make_password(self.password)
        # Save the updated User fields to the User table
        super().save(*args, **kwargs)


    
class Teacher(User):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    rfid_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='teacher_images/', null=True, blank=True)
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.role = User.Role.TEACHER

        # Update the User fields directly
        self.full_name = self.full_name
        self.rfid_number = self.rfid_number
        self.gender = self.gender
        self.phone_number = self.phone_number

        if self.assigned_class:
            # If a class is assigned, teacher is marked as class teacher
            self.is_class_teacher = True
        else:
            # If no class is assigned, teacher is not a class teacher
            self.is_class_teacher = False

        if self.password:
            self.password = make_password(self.password)
        # Save the updated User fields to the User table
        super().save(*args, **kwargs)

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=16)  # Secret key for TOTP
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        # Generate a TOTP using the secret key
        totp = pyotp.TOTP(self.otp_secret)
        return totp.now()

    def is_valid_otp(self, otp_entered):
        # Verify the entered OTP against the TOTP
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(otp_entered)

    def is_expired(self):
        # Check if OTP has expired (valid for 5 minutes)
        return (timezone.now() - self.created_at).total_seconds() > 300



class ApiKey(models.Model):
    key = models.CharField(max_length=100, unique=True)

    @staticmethod
    def generate():
        return ApiKey.objects.create(key=get_random_string(length=32))

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)