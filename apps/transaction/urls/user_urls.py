from django.urls import path

from apps.transaction.views.user_views import TransactionListAPIView

app_name = 'transaction_user'

urlpatterns = [
    path('list/', TransactionListAPIView.as_view(), name='list'),
]
