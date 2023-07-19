from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK
from django.utils import timezone
from django.utils.translation import gettext

from utils.response import ApiResponse

from apps.trc20.serializers.user_serializers import Trc20CreateGatewaySerializer
from apps.trc20.models import Trc20
from apps.purchase.models import Purchase
from apps.package.models import Package
from apps.invest.models import Invest
from apps.users.models import UserProfile
from apps.wallet.models import Wallet
from apps.network.models import Network

from apps.trc20.utils.coinremitter import create_invoice


class Trc20CreateGatewayAPIView(views.APIView):
    def post(self, request, format=None):
        user = self.request.user
        package_id = self.request.data['package']
        tether_amount = self.request.data['tether_amount']
        token_amount = self.request.data['token_amount']

        payment_gateway = create_invoice(tether_amount)

        payment_gateway_message = payment_gateway['msg']
        payment_gateway_data = payment_gateway['data']

        payment_gateway_invoice_id = payment_gateway_data['invoice_id']
        payment_gateway_merchant_id = payment_gateway_data['merchant_id']
        payment_gateway_total_amount = float(
            payment_gateway_data['total_amount']['USDTTRC20']
        )
        payment_gateway_address = payment_gateway_data['address']
        payment_gateway_url = payment_gateway_data['url']
        payment_gateway_symbol = payment_gateway_data['coin']
        payment_gateway_status = payment_gateway_data['status_code']

        package = Package.objects.get(id=package_id)

        purchase = Purchase.objects.create(
            user=user,
            package=package,
            tether_amount=tether_amount,
            token_amount=token_amount,
        )

        trc20 = Trc20.objects.create(
            user=user,
            purchase=purchase,
            message=payment_gateway_message,
            invoice_id=payment_gateway_invoice_id,
            merchant_id=payment_gateway_merchant_id,
            total_amount=payment_gateway_total_amount,
            address=payment_gateway_address,
            url=payment_gateway_url,
            symbol=payment_gateway_symbol,
            status=payment_gateway_status,
        )

        data = {
            'gateway_url': payment_gateway_url,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class Trc20NotifyGatewayAPIView(views.APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        try:
            status = self.request.data['status_code']

            # Paid or Overpaid
            if status == "1" or status == "3":
                invoice_id = self.request.data['invoice_id']
                amount = self.request.data['payment_history[0][amount]']
                payment_txid = self.request.data['payment_history[0][txid]']
                payment_confirmation = self.request.data['payment_history[0][confirmation]']

                trc20_obj = Trc20.objects.get(invoice_id=invoice_id)
                trc20_obj.status = status
                trc20_obj.paid_amount = amount
                trc20_obj.payment_txid = payment_txid
                trc20_obj.payment_confirmation = payment_confirmation
                trc20_obj.save()

                purchase_obj = trc20_obj.purchase
                purchase_obj.status = 'success'
                purchase_obj.save()

                user_obj = purchase_obj.user
                user_obj_profile = UserProfile.objects.get(
                    user=user_obj,
                )
                user_obj_network = Network.objects.get(
                    user=user_obj,
                )
                package_obj = purchase_obj.package
                package_obj_price = package_obj.price

                # Calculate total_invest
                total_invest = 0
                invest_list = Invest.objects.filter(
                    user=user_obj,
                    finished=False,
                )
                for invest in invest_list:
                    total_invest += invest.invest

                total_invest += package_obj_price

                user_obj_network.total_invest = total_invest
                user_obj_network.last_invest = package_obj_price
                user_obj_network.save()

                # Get token amount and minus from wallet
                token_amount = purchase_obj.token_amount
                if token_amount > 0.0:
                    token_wallet = Wallet.objects.get(
                        user=user_obj,
                        type='eit',
                    )
                    token_wallet.balance = float(
                        token_wallet.balance
                    ) - token_amount
                    token_wallet.save()

                invest_obj = Invest.objects.create(
                    user=user_obj,
                    package=package_obj,
                    invest=package_obj_price,
                    created_at=timezone.now(),
                )

                return Response({}, status=HTTP_200_OK)

            # Under paid
            elif status == "2":
                invoice_id = self.request.data['invoice_id']
                amount = self.request.data['payment_history[0][amount]']
                payment_txid = self.request.data['payment_history[0][txid]']
                payment_confirmation = self.request.data['payment_history[0][confirmation]']

                trc20_obj = Trc20.objects.get(invoice_id=invoice_id)
                trc20_obj.purchase.status = 'success'
                trc20_obj.status = status
                trc20_obj.paid_amount = amount
                trc20_obj.payment_txid = payment_txid
                trc20_obj.payment_confirmation = payment_confirmation
                trc20_obj.save()

                purchase_obj = trc20_obj.purchase
                purchase_obj.status = 'success'
                purchase_obj.save()

                user_obj = purchase_obj.user

                # Charge deposit wallet's balance
                wallet_obj = Wallet.objects.get(
                    user=user_obj,
                    type='deposit',
                )
                wallet_obj.balance = wallet_obj.balance + amount
                wallet_obj.save()

            else:
                return Response({}, status=HTTP_200_OK)

        except Exception as e:
            response = ApiResponse(
                success=False,
                code=500,
                error={
                    'code': str(e),
                    'detail': 'Server error',
                }
            )

            return Response(response, status=HTTP_200_OK)
