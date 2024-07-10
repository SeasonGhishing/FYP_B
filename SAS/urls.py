from django.contrib import admin
from django.urls import path, include
from SAS import settings
from accounts import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/announcements/', include('announcements.urls')),
    path('api/routine/', include('routine.urls')),
    path('api/classes/', include('classes.urls')),
    path('api/rfid/', include('RFID.urls')),
    path('admin_ui/', include('admin_ui.urls')),
    path('api/fcm/', include('fcm.urls')),
    path('', include('chat.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/leave_requests/', include('leave_requests.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
