from django.urls import path

from apps.trc20.views.user_views import Trc20CreateGatewayAPIView, Trc20NotifyGatewayAPIView

app_name = 'trc20_user'

urlpatterns = [
    path('create/', Trc20CreateGatewayAPIView.as_view(), name='create'),
    path('notify/', Trc20NotifyGatewayAPIView.as_view(), name='notify'),
]
