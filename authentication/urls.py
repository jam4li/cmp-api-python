from django.urls import path
from .api.views import TotpTemplateView, GenerateTOTPSecret, ValidateTOTPToken

app_name = 'authentication'
urlpatterns = [
    path('totp', TotpTemplateView.as_view(), name='totp'),
    path('generate-totp-secret/', GenerateTOTPSecret.as_view(),
         name='generate_totp_secret'),
    path('validate-totp-token/', ValidateTOTPToken.as_view(),
         name='validate_totp_token'),
]
