from django.urls import path

from .views import PackageListAPIView, PackageBuyAPIView

app_name = 'package'
urlpatterns = [
    path('', PackageListAPIView.as_view(), name='list'),
    path('buy/', PackageBuyAPIView.as_view(), name='buy'),
]
