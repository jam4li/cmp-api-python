from django.urls import path

from apps.network.views.user_views import NetworkTransactionListAPIView

app_name = 'network_user'

urlpatterns = [
    path(
        'transaction/list/',
        NetworkTransactionListAPIView.as_view(),
        name='transaction-list',
    ),
]
