from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.users.urls.user_urls')),
]
