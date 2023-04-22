from django.urls import path

from apps.package.views.user_views import PackageListAPIView, PackageBuyAPIView

app_name = 'package_user'

urlpatterns = [
    path('list/', PackageListAPIView.as_view(), name='list'),
    path('buy/', PackageBuyAPIView.as_view(), name='buy'),
]
