# from django.test import TestCase, Client
# from django.urls import reverse
# from rest_framework import status
# from .models import Class
# from .serializers import ClassSerializer

# class ClassAPITestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.class_data = {
#             'name': 'Test Class',
#             'description': 'This is a test class'
#         }
#         self.class_instance = Class.objects.create(**self.class_data)

#     def test_get_all_classes(self):
#         response = self.client.get(reverse('class-list-create'))
#         classes = Class.objects.all()
#         serializer = ClassSerializer(classes, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_create_class(self):
#         new_class_data = {
#             'name': 'New Class',
#             'description': 'This is a new class'
#         }
#         response = self.client.post(reverse('class-list-create'), new_class_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Class.objects.count(), 2)  # Assuming there's already one class created in setUp

#     def test_get_class_detail(self):
#         response = self.client.get(reverse('class-detail', kwargs={'pk': self.class_instance.pk}))
#         class_obj = Class.objects.get(pk=self.class_instance.pk)
#         serializer = ClassSerializer(class_obj)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_delete_class(self):
#         response = self.client.delete(reverse('class-detail', kwargs={'pk': self.class_instance.pk}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Class.objects.count(), 0)

#     def test_get_all_classes_failure(self):
#         # Test failure case where no classes exist
#         Class.objects.all().delete()
#         response = self.client.get(reverse('class-list-create'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 0)

#     def test_get_class_detail_failure(self):
#         # Test failure case where class with given ID doesn't exist
#         response = self.client.get(reverse('class-detail', kwargs={'pk': 999}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_delete_class_failure(self):
#         # Test failure case where class with given ID doesn't exist
#         response = self.client.delete(reverse('class-detail', kwargs={'pk': 999}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
