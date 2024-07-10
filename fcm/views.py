from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FCMToken
from .serializers import FCMTokenSerializer

class FCMTokenView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            fcm_token = FCMToken.objects.get(user=user)
            serializer = FCMTokenSerializer(fcm_token)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FCMToken.DoesNotExist:
            return Response({'error': 'FCM token not found'}, status=status.HTTP_404_NOT_FOUND)
