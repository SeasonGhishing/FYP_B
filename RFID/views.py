from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accounts.views import send_multiple_push_notifications, send_push_notification
from .models import RFID
from .serializers import RFIDSerializer


def get_latest_rfid_number():
    try:
        latest_rfid = RFID.objects.latest('rfid_number')
        return latest_rfid.rfid_number
    except RFID.DoesNotExist:
        return None


class RFIDAPIView(APIView):
    @csrf_exempt
    def post(self, request):
        rfid_data = request.data.get('rfid_data') 
        if rfid_data:  
            rfid_data = rfid_data.upper()  
            rfid_data_dict = {'rfid_number': rfid_data}
            serializer = RFIDSerializer(data=rfid_data_dict)
            if serializer.is_valid():
                serializer.save()
                # registration_tokens = ["euUWEphPRFeG2u3A2XP6kI:APA91bHyvyoOmjLwd24fzPSfcMprwLz-Lj_AhiqOtSzer4N3d-yWGeqfSNM1mqMHj9YNB65_-uu1FkME4WJrNti4WCpRMgKRY9J3OL2-osKl-X-VsM7XsN6LIe7q4fWH8TyR1LYIBaDh", "fKKgecIOTimxotms8BM04d:APA91bF3d32-PzEV3DU4Mv3YNthYywsw9wdrOyD4MzCecb4dDYPidIESP4aOxSSID7ScZZSEIDJwE0y6ceOSyol_aPYMyVPyseOBZ8cD1UIkJgS6PEMCIyCX1iC8hYKorD4YVWNeVNzH"]
                # message_title = "Your notification title"
                # message_body = "Your notification message"
                # send_multiple_push_notifications(registration_tokens,message_title,message_body)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'RFID data not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        rfids = RFID.objects.all()
        serializer = RFIDSerializer(rfids, many=True)
        return Response(serializer.data)
