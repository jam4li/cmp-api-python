from django.urls import path

from apps.referral.views.user_views import ReferralDirectListAPIView, ReferralBinaryDetailAPIView

app_name = 'referral_user'

urlpatterns = [
    path(
        'direct/list/',
        ReferralDirectListAPIView.as_view(),
        name='direct-list',
    ),
    path(
        'binary/detail/',
        ReferralBinaryDetailAPIView.as_view(),
        name='binary-detail',
    ),
]
