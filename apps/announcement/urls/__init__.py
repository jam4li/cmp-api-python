from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.announcement.urls.user_urls')),
]
