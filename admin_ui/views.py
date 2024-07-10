# views.py in your_frontend_app

from itertools import chain
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from RFID.models import RFID
from accounts.models import Student, Teacher
from announcements.models import Announcement
from django.shortcuts import render
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from classes.models import Class
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from leave_requests.models import LeaveRequest
from routine.models import Routine
from nepali_datetime import date as NepaliDate

def get_current_nepali_date():
    return str(NepaliDate.today().isoformat())


def base(request):
    return render(request, 'admin_ui/base.html')

# def dashboard(request):
#     classes = Class.objects.all().count()
#     students = Student.objects.all().count()
#     teachers = Teacher.objects.all().count()
#     return render(request, 'admin_ui/dashboard.html', {'classes': classes, 'students': students, 'teachers': teachers})

def dashboard(request):
    classes = Class.objects.all().count()
    students = Student.objects.all().count()
    teachers = Teacher.objects.all().count()
    
    # Get the current Nepali date
    today_nepali = get_current_nepali_date()
    
    # Calculate the attendance percentage
    people = students + teachers
    print("total are", people)
    total_people_today = Attendance.objects.filter(date=today_nepali).count()

    present_students_today = Attendance.objects.filter(date=today_nepali, status='L').count()
    
    if total_people_today > 0:
        attendance_percentage = (present_students_today / people) * 100
    else:
        attendance_percentage = 0

    context = {
        'classes': classes,
        'students': students,
        'teachers': teachers,
        'attendance_percentage': attendance_percentage,
    }
    
    return render(request, 'admin_ui/dashboard.html', context)

# def attendance(request):
#     attendances = Attendance.objects.all()
#     classes = Class.objects.all()
#     serializer = AttendanceSerializer(attendances, many=True)
#     print(serializer.data)  # Print serialized data
#     return render(request, 'admin_ui/attendance.html', {'attendances': serializer.data, 'classes': classes})

def attendance(request):
    attendances = Attendance.objects.all()
    classes = Class.objects.all()

    # Get filter parameters from request
    name_filter = request.GET.get('name', '')
    role_filter = request.GET.get('role', '')
    class_filter = request.GET.get('class', '')

    # Apply filters
    if name_filter:
        attendances = attendances.filter(user_details__full_name__icontains=name_filter)
    if role_filter:
        attendances = attendances.filter(user_details__role=role_filter)
    if class_filter:
        attendances = attendances.filter(user_details__assigned_class=class_filter)

    serializer = AttendanceSerializer(attendances, many=True)
    return render(request, 'admin_ui/attendance.html', {
        'attendances': serializer.data,
        'classes': classes,
        'name_filter': name_filter,
        'role_filter': role_filter,
        'class_filter': class_filter
    })



def leave_requests(request):
    current_date = timezone.now().date()

    # Filter leave requests for the current date
    leave_requests = LeaveRequest.objects.filter(created_at__date=current_date)
    teachers = Teacher.objects.all()
    students = Student.objects.all()
    return render(request, 'admin_ui/leaveRequests.html', {'leave_requests': leave_requests, 'teachers': teachers, 'students': students})

def routines(request):
    # routines = LeaveRequest.objects.all()
    return render(request, 'admin_ui/routines.html')



def student(request):
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
    
    return render(request, 'admin_ui/student_register.html', {'classes': classes, 'student_id': student_id, 'latest_rfid': latest_rfid, 'base_url': base_url})

def teacher(request):
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
    base_url = settings.BASE_URL 
    return render(request, 'admin_ui/teacher_register.html', {'classes': classes, 'teacher_id': teacher_id, 'latest_rfid': latest_rfid,'base_url': base_url})

def people(request):
    classes = Class.objects.all()
    teachers = Teacher.objects.all()
    students = Student.objects.all()
    people_list = list(chain(teachers, students))
    return render(request, 'admin_ui/people.html', {'people_list': people_list, 'classes': classes})

def routine_form(request):
    teachers = Teacher.objects.all()
    classes = Class.objects.all()
    routine_id = request.GET.get('id')


    return render(request, 'admin_ui/routine_form.html', {'teachers': teachers, 'classes': classes, 'routine_id': routine_id})

def routine_table(request):
    routines = Routine.objects.all()
    classes = Class.objects.all()
    return render(request, 'admin_ui/routine_table.html', {'routines': routines, 'classes': classes})


def announcement(request):
        latest_announcement = Announcement.objects.all().last()
        announcement = Announcement.objects.all()
        classes = Class.objects.all()
        return render(request, 'admin_ui/announcement.html', {'classes': classes, 'latest_announcement': latest_announcement, 'announcement': announcement})

def announcement_table(request):
        announcement = Announcement.objects.all()
        return render(request, 'admin_ui/announcement_table.html', {'announcement': announcement})

def attendance_view(request):
    # Get the current Nepali date
    today_nepali = get_current_nepali_date()
    
    # Assuming Attendance model has fields: student, date (in Nepali date format), status (e.g., 'present' or 'absent')
    total_students = Attendance.objects.filter(date=today_nepali).count()
    present_students = Attendance.objects.filter(date=today_nepali, status='present').count()
    
    if total_students > 0:
        attendance_percentage = (present_students / total_students) * 100
    else:
        attendance_percentage = 0

    return render(request, 'attendance.html', {
        'attendance_percentage': attendance_percentage
    })



