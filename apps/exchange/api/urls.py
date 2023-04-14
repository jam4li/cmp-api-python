from django.urls import path, include

from .views import *

app_name = 'exchange'
urlpatterns = [
    path('create/', ParentCreateAPIView.as_view(), name='parent-create'),
]
