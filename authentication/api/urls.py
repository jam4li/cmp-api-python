from django.urls import path

from .views import GetGoogleUrl, GoogleLogin, GenerateTOTPSecret, ValidateTOTPToken


app_name = 'authentication'
urlpatterns = [
    # GAuth
    path('google-url/', GetGoogleUrl.as_view(), name='google-url'),

    # Both
    path('callback/', GoogleLogin.as_view(), name='callback'),

    # 2fa
    path('security/2fa/get-form/', GenerateTOTPSecret.as_view(), name='get-form'),
    path('verify/', ValidateTOTPToken.as_view(), name='verify'),

    # TODO: auth/logout
]

# GET /admin/auth/google-url
# POST /admin/auth/verify
# PUT /admin/auth/callback
