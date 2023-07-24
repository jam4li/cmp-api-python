from django.utils import timezone

from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.withdraw.models import Withdraw
from apps.wallet.models import Wallet

from apps.withdraw.serializers.user_serializers import WithdrawListSerializer


class WithdrawListAPIView(views.APIView):
    """
    API view to fetch a list of withdrawal requests for the authenticated user.

    This view handles a GET request to retrieve a list of withdrawal requests for the authenticated user.

    Returns:
        - A JSON response containing a list of withdrawal requests for the user:
            - Withdrawal List (list): List of withdrawal requests, each represented as an object with withdrawal details.
                - "amount" (double): The amount of withdraw which equals to (requested_amount - fee)
                - "wallet_address" (str): The wallet address that the user wants the token to be sent in there
                - "transaction_hash" (str): If admin has sent the token to wallet, this field has been filled
                - "status" (str): rejected accepted pending
                - "wallet_type" (str): commission profit
                - "created_at" (datetime): When the withdraw request has been created
                - "update_at" (datetime): When the withdraw request has been updated

    Note:
        - The API expects a GET request to fetch a list of withdrawal requests for the authenticated user.
        - The authenticated user is considered the account holder for whom the withdrawal requests are retrieved.
        - The API queries the database for withdrawal requests made by the user.
        - The withdrawal requests are ordered by their creation date in descending order.
        - The serializer used to format the withdrawal list may vary based on the WithdrawListSerializer used.
        - The withdrawal list provides information about each withdrawal request, such as the withdrawal amount, status, etc.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "amount": 78.000,
                "wallet_address": "qwerty",
                "transaction_hash": "",
                "status": "pending",
                "wallet_type": "profit",
                "created_at": "2023-22-08",
                "updated_at": "",
            },
            {
                "amount": 100.000,
                "wallet_address": "qwerty",
                "transaction_hash": "qwerty",
                "status": "accepted",
                "wallet_type": "profit",
                "created_at": "2023-22-07",
                "updated_at": "2023-22-08",
            },
        ],
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        user = self.request.user

        withdraw_list = Withdraw.objects.filter(
            user=user,
        ).order_by(
            '-created_at',
        )

        serializer = WithdrawListSerializer(
            withdraw_list,
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


class WithdrawDetailAPIView(views.APIView):
    """
    API view to fetch withdrawal details including wallet's types and status for the authenticated user.

    This view handles a GET request to retrieve withdrawal details for the authenticated user.

    Returns:
        - A JSON response containing withdrawal details and available wallet types:
            - "wallet_types" (list): List of available wallet types for withdrawal, each represented as an object with type and display name.
                - "wallet_type" (str): commission profit.
                - "display_name" (str): Commission Profit.
            - "is_active" (bool): A boolean flag indicating whether the withdrawal functionality is active (True) or not (False).

    Note:
        - The API expects a GET request to fetch withdrawal details for the authenticated user.
        - The authenticated user is considered the account holder for whom the withdrawal details are retrieved.
        - The API retrieves the available wallet types for withdrawal from the Withdraw model's WALLET_TYPE_CHOICES.
        - The API sets the "is_active" flag to True, indicating that the withdrawal functionality is currently active.
        - The available wallet types and "is_active" status provide essential information for handling withdrawal requests.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": {
            "wallet_types": [
                {
                    "wallet_type": "commission",
                    "display_name": "Commission"
                },
                {
                    "wallet_type": "profit",
                    "display_name": "Profit"
                },
                ...
            ],
            "is_active": true
        },
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        wallet_types = [
            {
                'wallet_type': choice[0],
                'display_name': choice[1]
            }
            for choice in Withdraw.WALLET_TYPE_CHOICES
        ]

        data = {
            'wallet_types': wallet_types,
            'is_active': True,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class WithdrawCreateAPIView(views.APIView):
    """
    API view to create a withdrawal request for the authenticated user.

    This view handles a POST request to create a withdrawal request for the authenticated user.

    Parameters (in the POST request body):
        - 'wallet_address' (str): The address where the withdrawal amount will be sent.
        - 'wallet_type' (str): commission profit.
        - 'amount' (float): The amount to withdraw from the specified wallet.

    Returns:
        - A JSON response confirming the successful creation of the withdrawal request:
            - "message" (str): A success message indicating that the withdrawal request was created successfully.

    Note:
        - The API expects a POST request with the required parameters to create a withdrawal request for the authenticated user.
        - The authenticated user is considered the account holder who initiates the withdrawal.
        - The API calculates the withdrawal fee based on the provided wallet type and withdrawal amount:
            - If 'wallet_type' is 'commission', the fee is calculated as 10% of the withdrawal amount.
            - If 'wallet_type' is 'profit', the fee is a fixed amount of 2 Tether.
        - The API checks the balance of the specified wallet and verifies that it is sufficient to cover the withdrawal amount and fee.
        - If the fee is greater than the withdrawal amount or the wallet balance is insufficient, appropriate error responses are returned.
        - If the withdrawal request is valid, a Withdraw object is created in the database with 'pending' status and the provided details.
        - The API updates the wallet balance after deducting the withdrawal amount and fee.
        - The response confirms the successful creation of the withdrawal request.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "message": "Data retrieved successfully"
    }
    ```
    """

    def post(self, request, format=None):
        user = self.request.user
        wallet_address = self.request.data['wallet_address']
        wallet_type = self.request.data['wallet_type']
        amount = self.request.data['amount']

        amount = float(amount)

        # Calculate fee
        fee = 0

        if wallet_type == 'commission':
            fee = (10 * amount) / 100

        elif wallet_type == 'profit':
            fee = 2

        # Check wallet balance based on the wallet_type
        wallet = Wallet.objects.get(
            user=user,
            type=wallet_type,
        )

        wallet_balance = float(wallet.balance)

        if fee > amount:
            response = ApiResponse(
                success=False,
                code=402,
                error={
                    'code': 'fee greater than_amount',
                    'detail': 'Fee cannot be greater than the amount.',
                }
            )

            return Response(response)

        if wallet_balance < amount:
            response = ApiResponse(
                success=False,
                code=402,
                error={
                    'code': 'insufficient balance',
                    'detail': 'Insufficient balance in wallet',
                }
            )

            return Response(response)

        Withdraw.objects.create(
            user=user,
            amount=amount - fee,
            fee=fee,
            wallet_address=wallet_address,
            wallet_type=wallet_type,
            status='pending',
            created_at=timezone.now(),
        )

        wallet.balance = wallet_balance - (amount)
        wallet.updated_at = timezone.now()
        wallet.save()

        success_response = ApiResponse(
            success=True,
            code=200,
            message='Data retrieved successfully'
        )

        return Response(success_response)
