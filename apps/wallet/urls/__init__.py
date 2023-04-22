from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.wallet.urls.user_urls')),
]
