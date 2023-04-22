from django.urls import path

from apps.banner.views.user_views import BannerListAPIView

app_name = 'banner_user'

urlpatterns = [
    path('', BannerListAPIView.as_view(), name='list'),
]
