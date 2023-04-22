from django.urls import path

from apps.announcement.views.user_views import AnnouncementListAPIView

app_name = 'announcement_user'

urlpatterns = [
    path('list/', AnnouncementListAPIView.as_view(), name='list'),
]
