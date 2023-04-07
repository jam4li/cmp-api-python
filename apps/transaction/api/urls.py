from django.urls import path

from .views import TransactionListAPIView

app_name = 'transaction'
urlpatterns = [
    path('list/', TransactionListAPIView.as_view(), name='list'),
]
