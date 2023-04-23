from django.urls import path

from apps.referral.views.user_views import ReferralDirectListAPIView, ReferralBinaryDetailAPIView

app_name = 'referral_user'

urlpatterns = [
    path(
        'direct/list/',
        ReferralDirectListAPIView.as_view(),
    ),
    path(
        'binary/detail/',
        ReferralBinaryDetailAPIView.as_view(),
    ),
]
