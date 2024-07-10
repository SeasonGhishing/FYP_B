# views.py
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notifications.views import create_global_notification
from .models import Announcement
from .serializers import AnnouncementSerializer
    

class AnnouncementAPIView(APIView):
    def get(self, request):
        announcements = Announcement.objects.all()
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            announcement = serializer.save()
            target_class = announcement.target_class_id
            print(target_class)
            type = 'Announcement'
            message = 'Admin just posted an announcement'
            create_global_notification(target_class, type, message)
            redirect_url = reverse('base')
            return HttpResponseRedirect(redirect_url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnnouncementDetailAPIView(APIView):
    def get_announcement(self, pk):
        try:
            return Announcement.objects.get(pk=pk)
        except Announcement.DoesNotExist:
            return None

    def get(self, request, pk):
        announcement = self.get_announcement(pk)
        if announcement:
            serializer = AnnouncementSerializer(announcement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Announcement not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        announcement = self.get_announcement(pk)
        if announcement:
            announcement.delete()
            return Response({'message': 'Announcement deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Announcement not found'}, status=status.HTTP_404_NOT_FOUND)



