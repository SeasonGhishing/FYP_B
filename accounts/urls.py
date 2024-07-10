from django.urls import path, reverse

from SAS import settings
from .views import LoginView, LogoutView, PushNotificationView, ResetPasswordView, StudentAPIView, StudentDetailAPIView, TeacherAPIView, StudentListView, TeacherDetailAPIView,TeacherListView, GenerateOTPView, ValidateOTPView, ChangePasswordView, get_csrf_token_view, register_device
from accounts import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'accounts'

urlpatterns = [
    path('student_register_page/',views.student_register_page, name='student_register_page'),
    path('teacher_register_page/',views.teacher_register_page, name='teacher_register_page'),
    path('create-student/', csrf_exempt(StudentAPIView.as_view()), name='create-student'),
    path('create-teacher/', TeacherAPIView.as_view(), name='create-teacher'),
    path('students/<uuid:pk>/', StudentDetailAPIView.as_view(), name='student_detail'),
    path('teachers/<uuid:pk>/', TeacherDetailAPIView.as_view(), name='teacher_detail'),
    path('students-list/', StudentListView.as_view(), name='student-list-api'),
    path('teachers-list/', TeacherListView.as_view(), name='teacher-list-api'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('generate-otp/', GenerateOTPView.as_view(), name='generate_otp'),
    path('validate-otp/', ValidateOTPView.as_view(), name='validate_otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('send_push_notification/', PushNotificationView.as_view(), name='send_push_notification'),
    path('get-csrf-token/', get_csrf_token_view, name='get_csrf_token'),
    path('devices-register/', register_device, name='register_device'),
    # path('student-register/', views.register_page, name='student_registration'),
    # Add other paths as needed
]  

# reverse('accounts:student_registration')