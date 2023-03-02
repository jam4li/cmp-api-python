from django.urls import path

from .views import PackageListAPIView

app_name = 'package'
urlpatterns = [
    path('', PackageListAPIView.as_view(), name='list'),
]
