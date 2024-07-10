import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.utils import timezone

from accounts.models import Student, Teacher
from announcements.models import Announcement
from attendance.models import Attendance
from classes.models import Class
from leave_requests.models import LeaveRequest
from routine.models import Routine

@pytest.fixture
def create_class():
    return Class.objects.create(name="Maths")

@pytest.fixture
def create_student(create_class):
    return Student.objects.create(name="John Doe", class_id=create_class)

@pytest.fixture
def create_teacher(create_class):
    return Teacher.objects.create(name="Jane Doe", class_id=create_class)

@pytest.fixture
def create_attendance(create_student):
    return Attendance.objects.create(student=create_student, status="Present", date=timezone.now().date())

@pytest.fixture
def create_leave_request(create_teacher):
    return LeaveRequest.objects.create(teacher=create_teacher, reason="Personal", created_at=timezone.now())

@pytest.fixture
def create_routine(create_teacher, create_class):
    return Routine.objects.create(teacher=create_teacher, class_id=create_class, day="Monday", start_time="09:00", end_time="10:00")

@pytest.fixture
def create_announcement(create_class):
    return Announcement.objects.create(title="Test Announcement", content="This is a test announcement", class_id=create_class)

def test_dashboard(client, create_class, create_student, create_teacher):
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 200

def test_attendance(client, create_attendance):
    url = reverse('attendance')
    response = client.get(url)
    assert response.status_code == 200

def test_leave_requests(client, create_leave_request):
    url = reverse('leave_requests')
    response = client.get(url)
    assert response.status_code == 200

def test_routines(client):
    url = reverse('routines')
    response = client.get(url)
    assert response.status_code == 200

def test_student(client):
    url = reverse('student')
    response = client.get(url)
    assert response.status_code == 200

def test_teacher(client):
    url = reverse('teacher')
    response = client.get(url)
    assert response.status_code == 200

def test_people(client, create_student, create_teacher):
    url = reverse('people')
    response = client.get(url)
    assert response.status_code == 200

def test_routine_form(client, create_teacher, create_class):
    url = reverse('routine_form')
    response = client.get(url)
    assert response.status_code == 200

def test_routine_table(client, create_routine):
    url = reverse('routine_table')
    response = client.get(url)
    assert response.status_code == 200

def test_announcement(client, create_announcement):
    url = reverse('announcement')
    response = client.get(url)
    assert response.status_code == 200

def test_announcement_table(client, create_announcement):
    url = reverse('announcement_table')
    response = client.get(url)
    assert response.status_code == 200
