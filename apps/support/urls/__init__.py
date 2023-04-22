from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.support.urls.user_urls')),
]
