from django.urls import path, include

from .views import *

app_name = 'order'
urlpatterns = [
    # path('parent/list/', ParentListAPIView.as_view(), name='parent-list'),
    # path('parent/create/', ParentCreateAPIView.as_view(), name='parent-create'),
    # path('parent/status/change/', ParentStatusChangeAPIView.as_view(), name='parent-status-change'),
]