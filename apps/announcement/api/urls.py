from django.urls import path

from .views import AnnouncementListAPIView

app_name = 'announcement'
urlpatterns = [
    path('', AnnouncementListAPIView.as_view(), name='list'),
]
