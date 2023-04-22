from django.urls import path

from apps.authentication.views.user_views import GoogleLogin, GoogleCallback

app_name = 'authentication_user'

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
