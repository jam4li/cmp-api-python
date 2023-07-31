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
    '''
    API view for creating a payment gateway for TRC20 token purchases.

    Parameters:
        - 'package' (int): ID of the package being purchased.
        - 'tether_amount' (str): Amount of Tether (USDT) to be paid for the package.
        - 'token_amount' (str): Amount of EIT tokens to be received for the purchase.

    Returns:
        A JSON response containing the payment gateway URL and success message.

    Utility Functions:
        - create_invoice(tether_amount) - A utility function to create a payment gateway invoice in Coinremitter.
          It takes the 'tether_amount' as a parameter and returns the payment gateway response, which includes the gateway url.
    '''

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
    """
    API view for handling notifications from Coinremitter.

    This API view processes a POST request with the payment gateway's notification data to update the transaction status and user balances.

    Note:
        - This API handles different status codes received from the payment gateway and updates the relevant records accordingly.

    Parameters:
        - status_code (str): The status code received from the payment gateway indicating the transaction status.

    Returns:
        - HTTP_200_OK response with an empty JSON object because of payment gateway's docs.

    Raises:
        - HTTP_200_OK response with error details in JSON format if an exception occurs during processing.

    Flow:
        - For a status code of "1" or "3" (Paid or Overpaid), the view performs the following actions:
            1. Updates the TRC20 transaction details with the received payment information.
            2. Updates the purchase status to 'success'.
            3. Calculates the user's total investment and invest then updates the user network data accordingly.
            4. If there is a token amount associated with the purchase, it deducts the tokens from the user's wallet balance.
            5. Creates a new Invest record for the user and the corresponding package.

        - For a status code of "2" (Underpaid), the view performs the following actions:
            1. Updates the TRC20 transaction details with the received payment information.
            2. Updates the purchase status to 'success'.
            3. Charges the deposit wallet's balance by adding the received amount.

        - For any other status code, the view returns a successful HTTP_200_OK response with an empty JSON object.

    Utility Functions:
        - N/A (No additional utility functions are explicitly mentioned in the provided code snippet).

    """
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

                # Calculate total_active_invest and last_invest
                total_active_invest = 0
                invest_list = Invest.objects.filter(
                    user=user_obj,
                    finished=False,
                )
                for invest in invest_list:
                    total_active_invest += invest.invest

                total_active_invest += package_obj_price

                user_obj_network.total_active_invest = total_active_invest
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
