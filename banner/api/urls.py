from django.urls import path

from .views import BannerListAPIView

app_name = 'banner'
urlpatterns = [
    path('', BannerListAPIView.as_view(), name='list'),
]
