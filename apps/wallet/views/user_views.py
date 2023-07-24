from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.wallet.models import Wallet
from apps.wallet.serializers.user_serializers import WalletListSerializer


class WalletListAPIView(views.APIView):
    """
    API view to fetch a list of wallets associated with the authenticated user.

    This view handles a GET request to retrieve a list of wallets associated with the authenticated user.

    Returns:
        - A JSON response containing a list of wallets for the user:
            - Wallet List (list): List of wallets, each represented as an object with wallet details.
                - "title" (str): (e.g., 'Deposit Wallet')
                - "type" (str): deposit commission profit eit voucher
                - "access_type" (str): user company accounting
                - "balance" (double): Balance of wallet in double

    Note:
        - The API expects a GET request to fetch a list of wallets associated with the authenticated user.
        - The authenticated user is considered the account holder for whom the wallets are retrieved.
        - The API queries the database for wallets that belong to the user.
        - The serializer used to format the wallet list may vary based on the WalletListSerializer used.
        - The wallet list provides information about each wallet, such as the wallet type, balance, etc.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "title": "Profit Wallet",
                "type": "profit",
                "access_type": "user",
                "balance": 100.000,
            },
            {
                "title": "EIT Wallet",
                "type": "eit",
                "access_type": "user",
                "balance": 1000.000,
            },
            ...
        ],
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        user = self.request.user

        wallet = Wallet.objects.filter(
            user=user,
        )

        serializer = WalletListSerializer(
            wallet,
            many=True,
            context={"request": request},
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)
