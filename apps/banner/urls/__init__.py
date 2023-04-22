from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.banner.urls.user_urls')),
]
