from django.urls import path, include

from apps.exchange.views.user_views import *

app_name = 'exchange_user'

urlpatterns = [
    path('create/', ParentCreateAPIView.as_view(), name='parent-create'),
    path('detail/', ParentDetailAPIView.as_view(), name='parent-detail'),
]
