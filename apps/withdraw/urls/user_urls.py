from django.urls import path

from apps.withdraw.views.user_views import WithdrawListAPIView

app_name = 'withdraw_user'

urlpatterns = [
    path('list/', WithdrawListAPIView.as_view(), name='list'),
]
