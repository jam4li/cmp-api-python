from django.urls import path

from apps.wallet.views.user_views import WalletListAPIView

app_name = 'wallet_user'

urlpatterns = [
    path('list/', WalletListAPIView.as_view(), name='list'),
]
