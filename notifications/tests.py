# from django.test import TestCase, Client
# from django.urls import reverse
# from rest_framework import status
# from .models import Notification
# from accounts.models import Student, Teacher
# from .serializers import NotificationSerializer
# import jwt
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class NotificationAPITestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(email='test@example.com', password='password123')
#         self.notification1 = Notification.objects.create(users=self.user, notification_type='Type 1', message='Message 1')
#         self.notification2 = Notification.objects.create(users=self.user, notification_type='Type 2', message='Message 2')
        
#     def test_create_notification(self):
#         notification_data = {
#             'users': self.user.id,
#             'notification_type': 'Test Type',
#             'message': 'Test Message'
#         }
#         response = self.client.post(reverse('notification-list'), notification_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Notification.objects.count(), 3)

#     def test_get_all_notifications(self):
#         response = self.client.get(reverse('notification-list'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         notifications = Notification.objects.all()
#         serializer = NotificationSerializer(notifications, many=True)
#         self.assertEqual(response.data, serializer.data)

#     def test_get_notification_detail(self):
#         response = self.client.get(reverse('notification-detail', kwargs={'pk': self.notification1.id}))
#         notification = Notification.objects.get(pk=self.notification1.id)
#         serializer = NotificationSerializer(notification)
#         serializer_data = serializer.data
#         # Convert UUID object to string for comparison
#         serializer_data['users'] = str(serializer_data['users'])
#         response_data = response.data
#         # Convert UUID object to string for comparison
#         response_data['users'] = str(response_data['users'])
#         self.assertEqual(response_data, serializer_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

