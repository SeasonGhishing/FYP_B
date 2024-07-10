# from datetime import timedelta
# from django.test import TestCase
# from django.contrib.auth.hashers import check_password
# from django.utils import timezone
# from .models import Student, Teacher, OTP, ApiKey, PasswordResetOTP
# from django.contrib.auth import get_user_model

# from django.test import TestCase
# from django.urls import reverse
# from django.core import mail
# from rest_framework import status
# from rest_framework.test import APIClient
# from .models import PasswordResetOTP

# User = get_user_model()

# class GenerateOTPViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(email='test@example.com', password='password')

# class StudentModelTestCase(TestCase):
#     def test_create_student(self):
#         student = Student.objects.create(email='student@example.com', password='studentpassword')
#         self.assertEqual(student.email, 'student@example.com')
#         self.assertTrue(check_password('studentpassword', student.password))
#         self.assertEqual(student.role, 'Student')

# class TeacherModelTestCase(TestCase):
#     def test_create_teacher(self):
#         teacher = Teacher.objects.create(email='teacher@example.com', password='teacherpassword')
#         self.assertEqual(teacher.email, 'teacher@example.com')
#         self.assertTrue(check_password('teacherpassword', teacher.password))
#         self.assertEqual(teacher.role, 'Teacher')

# class ApiKeyModelTestCase(TestCase):
#     def test_generate_api_key(self):
#         api_key = ApiKey.generate()
#         self.assertIsNotNone(api_key)
#         self.assertIsNotNone(api_key.key)



# class GenerateOTPViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(email='test@example.com', password='password123')
#         url = reverse('accounts:generate_otp')
#         data = {'email': 'test@example.com'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(response.data.get('success', False))
#         self.generated_otp = None

#     def test_generate_otp_success(self):
#         url = reverse('accounts:generate_otp')
#         data = {'email': 'test@example.com'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(mail.outbox)
#         self.generated_otp = PasswordResetOTP.objects.last().otp

#     def test_generate_otp_email_not_exist(self):
#         url = reverse('accounts:generate_otp')
#         data = {'email': 'nonexistent@example.com'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_validate_correct_otp(self):
#         if not self.generated_otp:
#             self.test_generate_otp_success()

#         url = reverse('accounts:validate_otp') 
#         data = {'otp': self.generated_otp}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
