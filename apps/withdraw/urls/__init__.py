from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.withdraw.urls.user_urls')),
]
