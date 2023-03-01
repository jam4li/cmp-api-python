from django.urls import path

from .views import WalletListAPIView

app_name = 'wallet'
urlpatterns = [
    path('history/', WalletListAPIView.as_view(), name='history'),
]
