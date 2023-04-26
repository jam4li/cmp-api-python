from django.urls import path, include

from apps.exchange.views.user_views import *

app_name = 'exchange_user'

urlpatterns = [
    path(
        'bitmex/',
        CMEXBITApiView.as_view(),
        name='reject-user',
    ),
    path(
        'create/',
        ParentCreateAPIView.as_view(),
        name='parent-create',
    ),
    path(
        'detail/',
        ParentDetailAPIView.as_view(),
        name='parent-detail',
    ),
    path(
        'accept-user/<int:user_id>/',
        AcceptUserView.as_view(),
        name='accept-user',
    ),
    path(
        'reject-user/<int:user_id>/',
        RejectUserView.as_view(),
        name='reject-user',
    ),
]
