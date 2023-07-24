from django.urls import path

from apps.package.views.user_views import PackageListAPIView

app_name = 'package_user'

urlpatterns = [
    path('list/', PackageListAPIView.as_view(), name='list'),
]
