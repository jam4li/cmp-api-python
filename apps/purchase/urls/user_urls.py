from django.urls import path

from apps.purchase.views.user_views import PurchaseCalculateAPIView

app_name = 'purchase_user'

urlpatterns = [
    path(
        'calculate/',
        PurchaseCalculateAPIView.as_view(),
        name='calculate',
    ),
]
