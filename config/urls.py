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
        'api/v1/auth/',
        include('apps.authentication.api.urls', namespace='auth'),
    ),
    path(
        'api/v1/announcement/',
        include('apps.announcement.api.urls', namespace='announcement'),
    ),
    path(
        'api/v1/banner/',
        include('apps.banner.api.urls', namespace='banner'),
    ),
    path(
        'api/v1/exchange/',
        include('apps.exchange.api.urls', namespace='exchange'),
    ),
    path(
        'api/v1/invest/',
        include('apps.invest.api.urls', namespace='invest'),
    ),
    path(
        'api/v1/package/',
        include('apps.package.api.urls', namespace='package'),
    ),
    path(
        'api/v1/transaction/',
        include('apps.transaction.api.urls', namespace='transaction-api'),
    ),
    path(
        'api/v1/trc20/',
        include('apps.trc20.api.urls', namespace='trc20-api'),
    ),
    path(
        'api/v1/support/',
        include('apps.support.api.urls', namespace='support-api'),
    ),
    path(
        'api/v1/user/',
        include('apps.users.api.urls', namespace='user-api'),
    ),
    path(
        'api/v1/wallet/',
        include('apps.wallet.api.urls', namespace='wallet-api'),
    ),
    path(
        'api/v1/withdraw/',
        include('apps.withdraw.api.urls', namespace='withdraw-api'),
    ),
    path(
        '__debug__/',
        include('debug_toolbar.urls'),
    ),
]
