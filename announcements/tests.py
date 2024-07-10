# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from .models import Announcement
# from classes.models import Class
# from .serializers import AnnouncementSerializer
# import datetime

# class AnnouncementAPITestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.class_instance = Class.objects.create(name='Test Class')
#         self.announcement_data = {
#             'title': 'Test Announcement',
#             'content': 'This is a test announcement.',
#             'target_class': self.class_instance.id  # Pass the ID of the class
#         }

#     def test_create_announcement(self):
#         target_class_pk = self.class_instance.pk
#         self.announcement_data['target_class'] = target_class_pk
#         response = self.client.post(self.announcement_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_302_FOUND)


#     def test_get_announcement_list(self):
#         Announcement.objects.create(title='Announcement 1', content='Content 1', target_class=self.class_instance)
#         Announcement.objects.create(title='Announcement 2', content='Content 2', target_class=self.class_instance)
        
#         url = reverse('announcements:announcement-list')
#         response = self.client.get(url)
#         announcements = Announcement.objects.all()
#         serializer = AnnouncementSerializer(announcements, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_announcement_detail(self):
#         announcement = Announcement.objects.create(title='Announcement 1', content='Content 1', target_class=self.class_instance)
#         url = reverse('announcements:announcement-detail', kwargs={'pk': announcement.id})
#         response = self.client.get(url)
#         serializer = AnnouncementSerializer(announcement)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_delete_announcement(self):
#         announcement = Announcement.objects.create(title='Announcement 1', content='Content 1', target_class=self.class_instance)
#         url = reverse('announcements:announcement-detail', kwargs={'pk': announcement.id})
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
