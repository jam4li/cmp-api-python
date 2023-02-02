from django.urls import path

from .views import Trc20CreateGatewayAPIView, Trc20NotifyGatewayAPIView

app_name = 'trc20'
urlpatterns = [
    path('create/', Trc20CreateGatewayAPIView.as_view(), name='create-getway'),
    path('notify/', Trc20NotifyGatewayAPIView.as_view(), name='notify-getway'),
]
