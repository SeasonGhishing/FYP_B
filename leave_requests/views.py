import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from django.utils import timezone

    
class LeaveRequestDetailView(APIView):
    def get(self, request, pk):
        try:
            attendance = LeaveRequest.objects.get(pk=pk)
            serializer = LeaveRequestSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except LeaveRequest.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

class LeaveRequestAPIView(APIView):
    def post(self, request):
        # Extract requester ID from request data
        requester_id = request.data.get('requester')
        
        current_time = datetime.datetime.now().time()
        
        # Check if a request from the same requester ID exists for the current day
        today = timezone.now().date()
        existing_request = LeaveRequest.objects.filter(requester_id=requester_id, created_at__date=today).all()
        
        # if current_time < datetime.time(hour=7) or current_time >= datetime.time(hour=10):
        #     print("You cannot have a leave request at this moment")
        #     return Response({'error': 'You cannot have a leave request at this moment'}, status=status.HTTP_400_BAD_REQUEST)
        
        if existing_request:
            print("You already had")
            return Response({"error": "A leave request from this requester already exists for today."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LeaveRequestAllView(APIView):
    def get(self, request):
        leave_requests = LeaveRequest.objects.all()
        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data)
