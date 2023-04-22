from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.invest.urls.user_urls')),
]
