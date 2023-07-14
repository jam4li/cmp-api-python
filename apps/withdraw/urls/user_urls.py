from django.urls import path

from apps.withdraw.views.user_views import (
    WithdrawListAPIView,
    WithdrawDetailAPIView,
    WithdrawCreateAPIView,
)

app_name = 'withdraw_user'

urlpatterns = [
    path('list/', WithdrawListAPIView.as_view(), name='list'),
    path('detail/', WithdrawDetailAPIView.as_view(), name='detail'),
    path('create/', WithdrawCreateAPIView.as_view(), name='create'),
]
