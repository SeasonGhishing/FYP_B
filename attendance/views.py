import datetime
from itertools import chain
import time
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from accounts.views import send_push_notification
from fcm.models import FCMToken
from leave_requests.models import LeaveRequest
from notifications.views import create_notification
from .models import Attendance
from .serializers import AttendanceSerializer
from accounts.models import Student, Teacher, User
from django.contrib.auth import get_user_model
from nepali_datetime import date as NepaliDate

def get_current_nepali_date():
    return str(NepaliDate.today().isoformat())

class AttendanceSpecificAPIView(APIView):
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
            notifications = Attendance.objects.filter(user=user_id)
        else:
            notifications = Attendance.objects.all()
        serializer = AttendanceSerializer(notifications, many=True)
        return Response(serializer.data)


class AttendanceAllView(APIView):
    def get(self, request):
        attendance = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AttendanceTodayView(APIView):
    def get(self, request):
        today_nepali = get_current_nepali_date()
        attendance = Attendance.objects.filter(date=today_nepali)
        print(attendance, "is todays atc")
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AttendanceDetailView(APIView):
    def get(self, request, pk):
        try:
            attendance = Attendance.objects.get(pk=pk)
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)


class AttendanceView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        rfid = request.data.get('rfid_data')
        message = request.data.get('message')
        print(message)
        print(rfid)

        try:
            user = Student.objects.get(rfid_number=rfid)
        except Student.DoesNotExist:
            try:
                user = Teacher.objects.get(rfid_number=rfid)
            except Teacher.DoesNotExist:
                return Response({'error': 'User not found for the given RFID'}, status=status.HTTP_404_NOT_FOUND)

        current_time = datetime.datetime.now().time()
        
        # if datetime.datetime.today().weekday() == 5:
        #     return Response({'error': 'Attendance cannot be taken on Saturdays'}, status=status.HTTP_400_BAD_REQUEST)

        # if current_time < datetime.time(hour=9) or current_time >= datetime.time(hour=16, minute=30):
        #     return Response({'error': 'Attendance cannot be taken at the moment'}, status=status.HTTP_400_BAD_REQUEST)

        # if datetime.time(hour=16) <= current_time < datetime.time(hour=16, minute=30):
        #     pass

        today = get_current_nepali_date()
        print("today is ", today)

        # Check if the user has attendance entry for today
        attendance_entry = Attendance.objects.filter(user=user, date=str(today)).first()

        # Check if the user already has a pending status and it's not past 4 PM
        # if attendance_entry and attendance_entry.status != 'null' and current_time < datetime.time(hour=16):
        #     return Response({'error': 'Attendance already pending, please wait until 4 PM to try again'}, status=status.HTTP_400_BAD_REQUEST)

        if attendance_entry:
            if attendance_entry.exit_time:
                return Response({'error': 'Exit already recorded for today'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print('Setting exit time...')
                try:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print("Current Time =", current_time)
                    attendance_entry.exit_time = current_time
                    attendance_entry.status = 'P' if attendance_entry.status == 'Pen' else 'L'
                    attendance_entry.save()

                    # attendance_entry.exit_time = datetime.datetime.now()
                    # attendance_entry.status = 'P' if attendance_entry.status == 'Pen' else 'L'
                    # attendance_entry.save()

                    print('Exit time set successfully.')
                except Exception as e:
                    print(f'Error setting exit time: {e}')
                    return Response({'error': 'Failed to set exit time'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            message = "exited school"
        else:
            # Check if the current time is after 10:15 AM
            if current_time >= datetime.time(hour=16, minute=10):
                at_status = 'L'  # Late
            else:
                at_status = 'Pen'  # Pending

            try:
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                attendance_entry = Attendance.objects.create(user=user, entry_time=current_time, status=at_status)
                print('Entry time recorded.')
                if at_status == 'Pen':
                    message = "entered school"
                else:
                    message = "entered school but Late!"
            except Exception as e:
                print(f'Error creating attendance entry: {e}')
                return Response({'error': 'Failed to record entry time'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check if the status is 'Pen' (Pending) and exit time is recorded (i.e., present)
        if attendance_entry.status == 'Pen' and attendance_entry.exit_time:
            attendance_entry.status = 'P'  # Present

        try:
            fcm_token = FCMToken.objects.get(user=user).token
            first_name = user.full_name.split()[0]
            content = f"{first_name} just {message}"
            type = "Checked" if attendance_entry.status == 'P' else 'Warning'
            send_push_notification(fcm_token, "Attendance Update", message_body=content)
            create_notification(message=content, type=type, user_id=user.id)
        except FCMToken.DoesNotExist:
            print("FCM token not found for user")
        except Exception as e:
            print(f"Error sending push notification: {e}")

        return Response({'message': f'Attendance recorded: {message}'}, status=status.HTTP_200_OK)


class AbsentView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        User = get_user_model()
        message = request.data.get('message')
        print(message)
        
        if message:
            t = time.localtime() # Get current datetime object
            attendance_list = Attendance.objects.all()
            present_ids = [attendance.user.id for attendance in attendance_list] # Extract user IDs from attendance list
            print(present_ids)
            user_list = User.objects.values_list('id', flat=True).exclude(id__in=present_ids)  # Exclude present user IDs
            
            # Create Attendance entries for absent users
            for user_id in user_list:
                user_instance = User.objects.get(id=user_id)
                attendance_entry = Attendance.objects.create(
                    user=user_instance,
                    entry_time=None,  # Set entry time to current time as datetime object
                    exit_time=None,
                    status="A"
                )
            
            # You can customize the response as per your requirement
            response_data = {
                "message": "Absentees updated successfully"
            }
            
            return Response(response_data)

class InformedApiView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        User = get_user_model()
        leave_request_id = request.data.get('leave_request_id')
        print(leave_request_id)
        leave_request = get_object_or_404(LeaveRequest, pk=leave_request_id)
        requester = leave_request.requester.id
        action = request.data.get('action')

        if action == 'approve':
            leave_request.status = 'APPROVED'
        elif action == 'reject':
            leave_request.status = 'REJECTED'
        else:
            return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        leave_request.save()
        current_date = get_current_nepali_date()
        user = User.objects.get(id=requester)
        

        if leave_request.status == 'APPROVED':
            attendance_entry = Attendance.objects.create(
                    user=user,
                    date= str(current_date),
                    entry_time= None,
                    exit_time=None,
                    status="I"
                )

        response_data = {
                    "message": "Leave request status updated successfully"
                }
        create_notification(message="Your leave request got approved", type='Checked', user_id=user.id)
        
        return JsonResponse(response_data)
