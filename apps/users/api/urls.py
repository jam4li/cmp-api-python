from django.urls import path

from .views import UserDashboardAPIView, UserDetailAPIView

app_name = 'users'
urlpatterns = [
    path('dashboard/', UserDashboardAPIView.as_view(), name='dashboard'),
    path('detail/', UserDetailAPIView.as_view(), name='detail'),
]
