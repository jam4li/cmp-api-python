from django.urls import path, include

urlpatterns = [
    path('user/', include('apps.transaction.urls.user_urls')),
]
