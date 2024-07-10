from django.http import Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from RFID.models import RFID
from classes.models import Class
from fcm.models import FCMToken
from chat.models import ChatRoom
from .models import PasswordResetOTP, Student, Teacher, User
from .serializers import StudentSerializer, TeacherSerializer
from django.shortcuts import get_object_or_404, render
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
import random, string
from django.utils.translation import gettext_lazy as _
from firebase_admin import messaging
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ApiKey
from django.middleware.csrf import get_token
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

@csrf_exempt
def register_device(request):
    if request.method == 'POST':
        api_key = request.headers.get('Api-Key')
        if not api_key:
            return JsonResponse({'error': 'API key missing'}, status=401)
        if not ApiKey.objects.filter(key=api_key).exists():
            return JsonResponse({'error': 'Invalid API key'}, status=401)

        return JsonResponse({'success': True})

    elif request.method == 'GET':
        return JsonResponse({'message': 'GET request received'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)




def get_csrf_token_view(request):
    """
    View to return CSRF token as JSON response.
    """
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

def student_register_page(request):
    classes = Class.objects.all()  # Retrieve all classes
    student_id = request.GET.get('id')
    latest_rfid = None

    try:
        latest_rfid = RFID.objects.latest('created_at')
        if Student.objects.filter(rfid_number=latest_rfid.rfid_number).exists() or \
           Teacher.objects.filter(rfid_number=latest_rfid.rfid_number).exists():
            latest_rfid = None 
    except ObjectDoesNotExist:
        pass 

    base_url = settings.BASE_URL 
    
    return render(request, 'accounts/student_register.html', {'classes': classes, 'student_id': student_id, 'latest_rfid': latest_rfid, 'base_url': base_url})



def teacher_register_page(request):
    classes = Class.objects.all()
    teacher_id = request.GET.get('id')
    latest_rfid = None

    try:
       latest_rfid = RFID.objects.latest('created_at') 
       if Student.objects.filter(rfid_number=latest_rfid.rfid_number).exists() or \
           Teacher.objects.filter(rfid_number=latest_rfid.rfid_number).exists():
            latest_rfid = None
    except ObjectDoesNotExist:
        pass 
    return render(request, 'accounts/teacher_register.html', {'classes': classes, 'teacher_id': teacher_id, 'latest_rfid': latest_rfid})

class StudentAPIView(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            if student.assigned_class:
                class_teacher_id = student.assigned_class.teacher_id
                
                chat_room_exists = ChatRoom.objects.filter(students=student, teachers__id=class_teacher_id).exists()
                
                if not chat_room_exists:
                    teacher = Teacher.objects.get(id=class_teacher_id)
                    print(teacher, 'id is')
                    chat_room = ChatRoom.objects.create()
                    chat_room.students.add(student)
                    chat_room.teachers.add(teacher)
                    chat_room.save()
            redirect_url = reverse('base')        
            return HttpResponseRedirect(redirect_url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class StudentDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            # Check if 'assigned_class' is being updated
            if 'assigned_class' in serializer.validated_data:
                # Get the updated class teacher ID
                updated_class_teacher_id = serializer.validated_data['assigned_class'].teacher_id
                
                # Check if a chat room exists for the student and their current assigned class
                current_chat_room = ChatRoom.objects.filter(students=student, teachers__id=student.assigned_class.teacher_id).first()
                if current_chat_room:
                    # Delete the existing chat room associated with the current assigned class
                    current_chat_room.delete()
                
                # Check if a chat room already exists for the student and the updated assigned class's teacher
                chat_room_exists = ChatRoom.objects.filter(students=student, teachers__id=updated_class_teacher_id).exists()
                if not chat_room_exists:
                    # Create a new chat room and associate the student and teacher with it
                    teacher = Teacher.objects.get(id=updated_class_teacher_id)
                    chat_room = ChatRoom.objects.create()
                    chat_room.students.add(student)
                    chat_room.teachers.add(teacher)
                    chat_room.save()
            
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TeacherAPIView(APIView):
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            # Save the teacher
            teacher = serializer.save()
            
            # Retrieve the assigned class ID from the request data
            assigned_class_id = request.data.get('assigned_class', None)
            
            if assigned_class_id:
                # Retrieve the corresponding class instance
                assigned_class = get_object_or_404(Class, id=assigned_class_id)
                
                # Update the teacher_id field of the class with the teacher's ID
                assigned_class.teacher_id = teacher.id
                assigned_class.save()
            redirect_url = reverse('base')        
            return HttpResponseRedirect(redirect_url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeacherDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = TeacherSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = TeacherSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        student = self.get_object(pk)
        serializer = TeacherSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StudentListView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeacherListView(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        fcm_token = request.data.get('FCM-Token')

        if not email or not password:
            return Response({'error': 'Both email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if fcm_token:
            fcm_token_obj, created = FCMToken.objects.get_or_create(user=user)
            fcm_token_obj.token = fcm_token
            fcm_token_obj.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),  # Include the refresh token in the response
            'user_id': user.id,
            'role': user.role,
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



class GenerateOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            otp = ''.join(random.choices(string.digits, k=4))
            PasswordResetOTP.objects.create(user=User.objects.get(email=email), otp=otp)

            # Send OTP to the user's email
            subject = _('Password Reset OTP')
            message = f'Your OTP for password reset is: {otp}'
            from_email = 'raitomahang@gmail.com'  # Update with your email
            to_email = [email]
            send_mail(subject, message, from_email, to_email)

            return Response({'success': True})
        else:
            return HttpResponseNotFound({'success': False, 'message': _('Email does not exist')})

class ValidateOTPView(APIView):
    def post(self, request):
        otp_entered = request.data.get('otp')
        print('entered otp is: ', otp_entered)
        otp_obj = PasswordResetOTP.objects.latest('created_at')
        print("to validate: ", otp_obj.otp)
        if otp_obj.otp == otp_entered:
            # OTP is valid, proceed with the password reset process
            return Response({'success': True})
        else:
            return HttpResponseBadRequest({'success': False, 'message': _('Invalid OTP')})

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        otp_obj = PasswordResetOTP.objects.latest('created_at')
        print(email)
        print(new_password)
        print(confirm_password)
        print(otp_obj.otp, 'to validate')

        if not otp_obj:
            return HttpResponseBadRequest({'success': False, 'message': _('Invalid OTP')})

        if new_password != confirm_password:
            return HttpResponseBadRequest({'success': False, 'message': _('Passwords do not match')})

        # Reset password
        user = otp_obj.user
        user.set_password(new_password)
        user.save()

        # Delete the OTP
        otp_obj.delete()

        return Response({'success': True, 'message': _('Password reset successfully')})


class ChangePasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            
            # Check if the current password matches
            if check_password(current_password, user.password):
                # Set and save the new password
                user.set_password(new_password)
                user.save()
                return Response({'success': True, 'message': _('Password changed successfully')})
            else:
                return Response({'success': False, 'message': _('Current password is incorrect')})
        else:
            return Response({'success': False, 'message': _('Email does not exist')})
        
def send_push_notification(registration_token, message_title, message_body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=message_title,
            body=message_body,
        ),
        token=registration_token,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)
    
def send_multiple_push_notifications(registration_tokens, message_title, message_body):
    messages = []
    for token in registration_tokens:
        message = messaging.Message(
            notification=messaging.Notification(
                title=message_title,
                body=message_body,
            ),
            token=token,
        )
        messages.append(message)

class PushNotificationView(APIView):
    def post(self, request):
        registration_token = request.data.get('registration_token')
        message_title = request.data.get('message_title')
        message_body = request.data.get('message_body')

        if not registration_token or not message_title or not message_body:
            return Response({'error': 'registration_token, message_title, and message_body are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            send_push_notification(registration_token, message_title, message_body)
            return Response({'message': 'Push notification sent successfully'},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

