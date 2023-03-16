"""cmp_api_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path(
        '',
        include('apps.dashboard.urls', namespace='dashboard'),
    ),
    path(
        'admin/',
        admin.site.urls,
    ),
    path(
        'auth/',
        include('apps.authentication.api.urls', namespace='auth'),
    ),
    path(
        'security/',
        include('apps.authentication.api.urls', namespace='security'),
    ),
    path(
        'api/announcement/',
        include('apps.announcement.api.urls', namespace='announcement'),
    ),
    path(
        'api/banner/',
        include('apps.banner.api.urls', namespace='banner'),
    ),
    path(
        'api/invest/',
        include('apps.invest.api.urls', namespace='invest'),
    ),
    path(
        'api/package/',
        include('apps.package.api.urls', namespace='package'),
    ),
    path(
        'api/trc20/',
        include('apps.trc20.api.urls', namespace='trc20-api'),
    ),
    path(
        'api/wallet/',
        include('apps.wallet.api.urls', namespace='wallet-api'),
    ),
    path(
        'sentry-debug/',
        trigger_error,
    ),
]
