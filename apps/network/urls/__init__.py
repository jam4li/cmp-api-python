from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.network.urls.user_urls')),
]
