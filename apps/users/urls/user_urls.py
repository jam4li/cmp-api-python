from django.urls import path

from apps.users.views.user_views import (
    UserDashboardAPIView,
    UserDetailAPIView,
    UserCreateAPIView,
    UserReferralDetailAPIView
)

app_name = 'users_user'

urlpatterns = [
    path('dashboard/', UserDashboardAPIView.as_view(), name='dashboard'),
    path('detail/', UserDetailAPIView.as_view(), name='detail'),
    path('create/', UserCreateAPIView.as_view(), name='create'),
    path('referral/', UserReferralDetailAPIView.as_view(), name='referral'),
]
