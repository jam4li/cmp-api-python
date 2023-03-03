from django.urls import path

from .views import GetGoogleUrl, GoogleLogin, GenerateTOTPSecret, ValidateTOTPToken


app_name = 'authentication'
urlpatterns = [
    # 2fa - it get triggered when at first they want to toggle user.enable_google_2fa_verification and generates a TOTP secret and qrCode
    path('security/2fa/get-form/', GenerateTOTPSecret.as_view(), name='get-form'),

    # GAuth
    path('google-url/', GetGoogleUrl.as_view(), name='google-url'),

    # Both
    path('callback/', GoogleLogin.as_view(), name='callback'),

    # 2fa
    path('verify/', ValidateTOTPToken.as_view(), name='verify'),

    # TODO: auth/logout
]

# GET /admin/auth/google-url
# POST /admin/auth/verify
# PUT /admin/auth/callback
