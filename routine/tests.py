# from unittest.mock import patch
# from django.test import TestCase, Client
# from django.urls import reverse
# from rest_framework import status
# from .models import Routine
# from accounts.models import Teacher
# from classes.models import Class
# from .serializers import RoutineSerializer

# from datetime import time

# class RoutineAPITestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.teacher = Teacher.objects.create(email='teacher@example.com', password='password123')
#         self.class_instance = Class.objects.create(name='Test Class')
#         self.routine1 = Routine.objects.create(subject='Math', assigned_teacher=self.teacher, start_time=time(8, 0), end_time=time(9, 0), target_class=self.class_instance, day_of_week='Mon')
#         self.routine2 = Routine.objects.create(subject='Science', start_time=time(9, 0), end_time=time(10, 0), target_class=self.class_instance, day_of_week='Tue')

        
#     @patch('routine.models.Routine.save')
#     def test_create_routine(self, mock_save):
#         routine_data = {
#             'subject': 'History',
#             'assigned_teacher': self.teacher.id,
#             'start_time': '10:00:00',
#             'end_time': '11:00:00',
#             'target_class': self.class_instance.id,
#             'day_of_week': 'Wed'
#         }
#         response = self.client.post(reverse('routine:routine-list-create'), routine_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_302_FOUND)
#         self.assertEqual(Routine.objects.count(), 2)
#         mock_save.assert_called_once()

#     def test_get_all_routines(self):
#         response = self.client.get(reverse('routine:routines'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         routines = Routine.objects.all()
#         serializer = RoutineSerializer(routines, many=True)
#         for data in serializer.data:
#             data['start_time'] = str(data['start_time'])
#             data['end_time'] = str(data['end_time'])
#         self.assertEqual(response.data, serializer.data)


#     def test_get_routine_detail(self):
#         response = self.client.get(reverse('routine:routine-detail', kwargs={'pk': self.routine1.id}))
#         routine = Routine.objects.get(pk=self.routine1.id)
#         serializer = RoutineSerializer(routine)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_routine(self):
#         updated_data = {
#             'start_time': '10:30:00',
#             'end_time': '11:30:00',
#             'day_of_week': 'Fri'
#         }
#         response = self.client.patch(reverse('routine:routine-detail', kwargs={'pk': self.routine1.id}), updated_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
#         self.routine1.refresh_from_db()
#         self.assertEqual(self.routine1.start_time.strftime('%H:%M:%S'), '10:30:00')
#         self.assertEqual(self.routine1.end_time.strftime('%H:%M:%S'), '11:30:00')
#         self.assertEqual(self.routine1.day_of_week, 'Fri')

#     def test_delete_routine(self):
#         response = self.client.delete(reverse('routine:routine-detail', kwargs={'pk': self.routine1.id}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Routine.objects.count(), 1)

