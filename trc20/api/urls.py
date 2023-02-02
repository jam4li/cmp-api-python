from django.urls import path

from .views import Trc20CreateGatewayAPIView

app_name = 'trc20'
urlpatterns = [
    path('create/', Trc20CreateGatewayAPIView.as_view(), name='create-getway'),
]
