from django.urls import path

from .views import WithdrawListAPIView

app_name = 'withdraw'
urlpatterns = [
    path('list/', WithdrawListAPIView.as_view(), name='list'),
]
