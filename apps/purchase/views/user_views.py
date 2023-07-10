from rest_framework import views
from rest_framework.response import Response
from django.utils.translation import gettext

from utils.response import ApiResponse

from apps.purchase.models import Purchase
from apps.package.models import Package
from apps.wallet.models import Wallet


class PurchaseCalculateAPIView(views.APIView):
    def post(self, request, format=None):
        user = self.request.user
        package_id = self.request.data['package']
        percent = self.request.data['percent']

        package = Package.objects.get(id=package_id)
        package_price = round(float(package.price), 2)
        package_fee = round(float(package.fee), 2)

        token_in_usdt = (int(percent) * package_price) / 100
        token_in_usdt = round(float(token_in_usdt), 2)
        token_percent = int(percent)

        token_amount = int(token_in_usdt * 4)

        tether_amount = int(package_price - token_in_usdt)
        tether_amount += package_fee
        tether_percent = int(100 - token_percent)

        token_wallet = Wallet.objects.get(
            user=user,
            type='cmp',
        )
        token_wallet_balance = token_wallet.balance

        if token_amount > token_wallet_balance:
            response = ApiResponse(
                success=False,
                code=402,
                error={
                    'code': 'insufficient balance',
                    'detail': 'Insufficient balance in EIT wallet',
                }
            )

            return Response(response)

        data = {
            "package_price": package_price,
            "token_amount": token_amount,
            "token_percent": token_percent,
            "tether_amount": tether_amount,
            "tether_percent": tether_percent,
            "fee": fee,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)
