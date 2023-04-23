from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.referral.urls.user_urls')),
]
