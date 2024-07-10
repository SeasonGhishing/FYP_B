# urls.py in your_frontend_app

from django.urls import path
from accounts.views import student_register_page, teacher_register_page
from admin_ui import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('people/', views.people, name='people'),
    path('attendance/', views.attendance, name='attendance'),
    path('leaveRequests/', views.leave_requests, name='leave_requests'),
    path('announcement/', views.announcement, name='announcement'),
    path('announcement_table/', views.announcement_table, name='announcement_table'),
    path('routines/', views.routines, name='routines'),
    path('routine_form/', views.routine_form, name='routine'),
    path('routine_table/', views.routine_table, name='routine'),
    path('teacher/', views.teacher, name='teacher'),
    path('student/', views.student, name='student'),
    path('student_register_page/',student_register_page, name='student_register_page'),
    path('teacher_register_page/',teacher_register_page, name='teacher_register_page'),
    # Add more paths for other frontend views
]
