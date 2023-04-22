from django.urls import path

from apps.invest.views.user_views import InvestListAPIView

app_name = 'invest_user'

urlpatterns = [
    path('list/', InvestListAPIView.as_view(), name='list'),
]
