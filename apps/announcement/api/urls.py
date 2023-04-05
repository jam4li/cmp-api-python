from django.urls import path

from .views import AnnouncementListAPIView

app_name = 'announcement'
urlpatterns = [
    path('list/', AnnouncementListAPIView.as_view(), name='list'),
]
