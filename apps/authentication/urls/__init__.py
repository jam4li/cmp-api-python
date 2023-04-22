from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.authentication.urls.user_urls')),
]
