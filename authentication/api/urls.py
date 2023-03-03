from django.urls import path

from .views import GoogleLogin, GenerateTOTPSecret, ValidateTOTPToken


app_name = 'authentication'
urlpatterns = [
    path('security/2fa/get-form/', GenerateTOTPSecret.as_view(), name='get-form'),

    path('google-url/', GoogleLogin.as_view(), name='google-url'),
    path('callback/', GoogleLogin.as_view(), name='callback'),
    path('verify/', ValidateTOTPToken.as_view(), name='verify'),
    # auth/logout
]

# GET /admin/auth/google-url
# POST /admin/auth/verify
# PUT /admin/auth/callback
