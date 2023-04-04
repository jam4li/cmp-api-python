from django.urls import path

from .views import GoogleLogin, GoogleCallback

app_name = 'authentication'
urlpatterns = [
    path(
        'google-url/',
        GoogleLogin.as_view(),
        name='google-url',
    ),
    path(
        'callback/',
        GoogleCallback.as_view(),
        name='callback',
    ),
]
