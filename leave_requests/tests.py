# from django.test import TestCase, Client
# from django.urls import reverse
# from rest_framework import status
# from .models import LeaveRequest
# from .serializers import LeaveRequestSerializer
# # from django.contrib.auth.models import User
# from accounts.models import Student, Teacher
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class LeaveRequestAPITestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user( email='test@example.com', password='password123')
#         self.student = Student.objects.create(full_name='Test Student', rfid_number='1234567890', gender='Male', phone_number='1234567890', parent_name='Parent')
#         self.leave_request_data = {
#             'requester': self.user,
#             'reason': 'Personal',
#             'description': 'Personal reasons',
#             'status': 'PENDING'
#         }
#         self.leave_request = LeaveRequest.objects.create(**self.leave_request_data)

#     def test_create_leave_request(self):
#         response = self.client.post(reverse('leave-request'), self.leave_request_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(LeaveRequest.objects.count(), 2)  # Assuming there's already one leave request created in setUp

#     def test_get_leave_request_detail(self):
#         response = self.client.get(reverse('leave-request', kwargs={'pk': self.leave_request.id}))
#         leave_request_obj = LeaveRequest.objects.get(pk=self.leave_request.id)
#         serializer = LeaveRequestSerializer(leave_request_obj)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_leave_request_detail_failure(self):
#         response = self.client.get(reverse('leave-request', kwargs={'pk': 999}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_get_all_leave_requests(self):
#         response = self.client.get(reverse('leave-request'))
#         leave_requests = LeaveRequest.objects.all()
#         serializer = LeaveRequestSerializer(leave_requests, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
