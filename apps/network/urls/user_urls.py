from django.urls import path

from apps.network.views.user_views import (
    NetworkTransactionListAPIView,
    NetworkDirectListAPIView,
    NetworkBinaryDetailAPIView,
    NetworkDetailAPIView,
)

app_name = 'network_user'

urlpatterns = [
    path(
        'detail/',
        NetworkDetailAPIView.as_view(),
        name='detail',
    ),
    path(
        'direct/list/',
        NetworkDirectListAPIView.as_view(),
        name='direct-list',
    ),
    path(
        'binary/detail/',
        NetworkBinaryDetailAPIView.as_view(),
        name='binary-detail',
    ),
    path(
        'transaction/list/',
        NetworkTransactionListAPIView.as_view(),
        name='transaction-list',
    ),
]
