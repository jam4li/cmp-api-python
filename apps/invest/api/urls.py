from django.urls import path

from .views import InvestListAPIView

app_name = 'invest'
urlpatterns = [
    path('<str:status>/', InvestListAPIView.as_view(), name='list'),
]
