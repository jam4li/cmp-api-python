from rest_framework import views
from rest_framework.response import Response
from django.utils.translation import gettext

from utils.response import ApiResponse

from apps.purchase.models import Purchase
from apps.package.models import Package
from apps.wallet.models import Wallet


class PurchaseCalculateAPIView(views.APIView):
    """
    API view to calculate the details of a package purchase based on the selected percentage.

    This view handles a POST request to calculate the details of a package purchase based on the provided
    package ID and percentage. It calculates the EIT amount and Tether amount based on the selected percentage,
    and verifies if the user has sufficient balance in their EIT wallet to complete the purchase.

    Parameters:
        - "package" (int): The ID of the selected package for purchase.
        - "percent" (int): The percentage of the package price to be paid in tokens.

    Returns:
        - A JSON response containing the calculated purchase details:
            - "package_price" (double): The price of the selected package in USDT.
            - "token_amount" (double): The calculated amount of tokens to be paid based on the selected percentage.
            - "token_percent" (int): The percentage of the package price paid in tokens.
            - "tether_amount" (double): The calculated amount of USDT to be paid based on the selected percentage.
            - "tether_percent" (int): The percentage of the package price paid in USDT.
            - "fee" (double): The fee associated with the selected package in USDT.

    Note:
        - The API expects a POST request containing the package ID and the percentage of the package price
          to be paid in tokens.
        - The package ID is used to fetch the corresponding package details from the 'Package' model.
        - The 'percent' parameter is used to calculate the EIT amount and Tether amount based on the selected
          percentage of the package price.
        - The calculated EIT amount is four times the calculated token value in USDT (Each EIT is 0.25 Tether).
        - The API verifies if the user has sufficient balance in their EIT wallet to complete the purchase.
        - If the user's EIT wallet balance is insufficient, the API returns a 'insufficient balance' response.

    Example Response:
    ```
    HTTP 200 OK
    {
        "package_price": 100.0,
        "token_amount": 200.000,
        "token_percent": 50,
        "tether_amount": 50.000,
        "tether_percent": 50,
        "fee": 5.0
    }
    ```
    """

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
            type='eit',
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
            "fee": package_fee,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)
