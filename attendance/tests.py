# import datetime
# from django.test import TestCase, Client
# from django.urls import reverse
# from rest_framework import status

# from classes.models import Class
# from .models import Attendance
# from accounts.models import Student, Teacher
# from accounts.serializers import StudentSerializer, TeacherSerializer
# from django.test import TestCase
# from django.contrib.auth import get_user_model



# User = get_user_model()

# class TeacherModelTestCase(TestCase):
#     def setUp(self):
#         self.class_instance = Class.objects.create(name='Mathematics')
#         self.teacher = Teacher.objects.create(
#             email='teacher1@example.com',
#             password='password123',
#             full_name='John Doe',
#             rfid_number='1234567890',
#             gender='Male',
#             phone_number='1234567890',
#             assigned_class=self.class_instance
#         )

#     def test_teacher_creation(self):
#         self.assertEqual(self.teacher.email, 'teacher1@example.com')
#         self.assertTrue(self.teacher.check_password('password123'))
#         self.assertEqual(self.teacher.full_name, 'John Doe')
#         self.assertEqual(self.teacher.rfid_number, '1234567890')
#         self.assertEqual(self.teacher.gender, 'Male')
#         self.assertEqual(self.teacher.phone_number, '1234567890')
#         self.assertEqual(self.teacher.assigned_class, self.class_instance)

# class StudentModelTestCase(TestCase):
#     def setUp(self):
#         self.class_instance = Class.objects.create(name='Science')
#         self.student = Student.objects.create(
#             email='student1@example.com',
#             password='password123',
#             full_name='Jane Doe',
#             rfid_number='0987654321',
#             gender='Female',
#             phone_number='9876543210',
#             parent_name='Alice Doe',
#             assigned_class=self.class_instance
#         )

#     def test_student_creation(self):
#         self.assertEqual(self.student.email, 'student1@example.com')
#         self.assertTrue(self.student.check_password('password123'))
#         self.assertEqual(self.student.full_name, 'Jane Doe')
#         self.assertEqual(self.student.rfid_number, '0987654321')
#         self.assertEqual(self.student.gender, 'Female')
#         self.assertEqual(self.student.phone_number, '9876543210')
#         self.assertEqual(self.student.parent_name, 'Alice Doe')
#         self.assertEqual(self.student.assigned_class, self.class_instance)


# class AttendanceAPITestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.class_instance = Class.objects.create(name='Test Class')
#         self.student = Student.objects.create(
#             email='student@example.com',
#             password='password123',
#             full_name='John Doe',
#             rfid_number='1234567890',
#             gender='Male',
#             phone_number='1234567890',
#             parent_name='Alice Doe',
#             assigned_class=self.class_instance
#         )
        
#     def test_invalid_rfid(self):
#         invalid_data = {
#             'rfid_data': '00000',  # Invalid RFID
#             'message': 'Test message for invalid RFID'
#         }
#         response = self.client.post(reverse('attendance-create'), invalid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(Attendance.objects.count(), 0)
