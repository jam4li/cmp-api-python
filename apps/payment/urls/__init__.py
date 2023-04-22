from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.payment.urls.user_urls')),
]
