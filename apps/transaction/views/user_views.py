from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.transaction.models import Transaction
from apps.transaction.serializers.user_serializers import TransactionListSerializer


class TransactionListAPIView(views.APIView):
    """
    API view to fetch a list of transactions for the authenticated user.

    This view handles a GET request to retrieve a list of transactions for the authenticated user.

    Returns:
        - A JSON response containing a list of transactions for the user:
            - Transaction List (list): List of transactions, each represented as an object with transaction details.
                - "amount" (double): The amount of transaction.
                - "type" (str): profit binary direct
                - "description" (str): The description about the transaction
                - "updated_at" (datetime): When the transaction has been updated

    Note:
        - The API expects a GET request to fetch a list of transactions for the authenticated user.
        - The authenticated user is considered the account holder for whom the transactions are retrieved.
        - The API queries the database for transactions that belong to the user.
        - The transactions are ordered by their creation date in ascending order.
        - The serializer used to format the transaction list may vary based on the TransactionListSerializer used.
        - The transaction list provides information about each transaction, such as the transaction type, amount, etc.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "amount": 100.000,
                "type": "profit",
                "description": "Daily profit of 100.000$",
                "updated_at": "2023-07-22 03:30:00" 
            },
            {
                "amount": 200.000,
                "type": "profit",
                "description": "Daily profit of 200.000$",
                "updated_at": "2023-07-22 03:30:00" 
            },
        ],
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        user = self.request.user

        transaction_list = Transaction.objects.filter(
            user=user,
        ).order_by(
            'created_at',
        )

        serializer = TransactionListSerializer(
            transaction_list,
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
