from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.package.urls.user_urls')),
]
