from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.trc20.urls.user_urls')),
]
