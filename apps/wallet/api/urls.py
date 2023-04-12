from django.urls import path

from .views import WalletListAPIView

app_name = 'wallet'
urlpatterns = [
    path('list/', WalletListAPIView.as_view(), name='list'),
]
