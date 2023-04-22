from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.exchange.urls.user_urls')),
]
