import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Student, Teacher, User
from accounts.views import send_multiple_push_notifications
from fcm.models import FCMToken
from .models import Notification
from .serializers import NotificationSerializer
from django.shortcuts import get_object_or_404

class NotificationListAPIView(APIView):
    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationDetailAPIView(APIView):
    def get(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def delete(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NotificationSpecificAPIView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization', '').split(' ')[1]  # Assuming the token is in the format "Bearer <token>"

        # Decode the token to get user ID
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            user_id = decoded_token.get('user_id')
        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = get_object_or_404(User, id=user_id)
        
        if user:
            notifications = Notification.objects.filter(users=user_id)
        else:
            notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
def create_notification(type, message, user_id):
    notification = Notification(notification_type=type, message=message, users_id=user_id)
    notification.save()
    
def create_global_notification(target_class, type, message):
    if target_class != None:
        teachers = Teacher.objects.filter(assigned_class=target_class)            
        students = Student.objects.filter(assigned_class=target_class)
        users = list(teachers) + list(students)
        fcm_tokens = FCMToken.objects.filter(user_id__in=[user.id for user in users])
        tokens = [token.token for token in fcm_tokens]
        # print(tokens)

        send_multiple_push_notifications(tokens, type, message)

        notification_message = message
        for user in users:
            # Create and save notifications for users
            notification = Notification(notification_type=type, message=notification_message, users_id=user.id)
            notification.save()
    else:
        users = User.objects.all()
        notification_message = message
        for user in users:
            notification = Notification(notification_type=type, message=message, users_id=user.id)
            notification.save()
        