from django.utils.translation import gettext_lazy as _
from rest_framework import views, status
from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.network.models import Network, NetworkTransaction
from apps.network.serializers.user_serializers import (
    NetworkBinaryDetailSerializer,
    NetworkDirectListSerializer,
    NetworkTransactionListSerializer,
)


class NetworkTransactionListAPIView(views.APIView):
    """
    API view to fetch a list of network transactions for the authenticated user.

    This view handles a GET request to retrieve a list of network transactions for the authenticated user.

    Returns:
        - A JSON response containing a list of network transactions for the user:
            - Network Transaction List (list): List of network transactions, each represented as an object with transaction details.
                - "type" (str): binary direct profit
                - "amount" (double): The amount of network transaction
                - "day" (int): Number of day for the network transaction
                - "description" (str): The description about the network transaction
                - "created_at" (datetime): When the network transaction has been created

    Note:
        - The API expects a GET request to fetch a list of network transactions for the authenticated user.
        - The authenticated user is considered the account holder for whom the network transactions are retrieved.
        - The API queries the database for network transactions that belong to the user.
        - The serializer used to format the network transaction list may vary based on the NetworkTransactionListSerializer used.
        - The network transaction list provides information about each transaction, such as transaction type, amount, date, etc.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "type": "profit",
                "amount": 1.000,
                "day": 1,
                "description": "Daily profit of 100.000$",
                "created_at": "2023-07-20"
            },
            {
                "type": "binary",
                "amount": 5.000,
                "day": 1,
                "description": "Binary of user abcd",
                "created_at": "2023-07-21"
            },
        ],
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        user = self.request.user

        network_transaction_list = NetworkTransaction.objects.filter(
            user=user,
        ).order_by(
            '-id',
        )

        serializer = NetworkTransactionListSerializer(
            network_transaction_list,
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


class NetworkDirectListAPIView(views.APIView):
    """
    API view to fetch a list of directly referred members in the user's network.

    This view handles a GET request to retrieve a list of directly referred members in the user's network.

    Returns:
        - A JSON response containing a list of directly referred members in the user's network:
            - Direct Referral List (list): List of directly referred members, each represented as an object with member details.
                - user (str): The email of the user
                - side (str): left right

    Note:
        - The API expects a GET request to fetch a list of directly referred members in the user's network.
        - The user making the request is considered the referrer who directly referred the members.
        - The API queries the database for network members whose 'referrer' field matches the user making the request.
        - The serializer used to format the direct referral list may vary based on the NetworkDirectListSerializer used.
        - The direct referral list provides information about each member, such as member's email, side.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "user": "test@gmail.com",
                "side": "left",
            },
            {
                "user": "test2@gmail.com",
                "side": "right",
            },
        ],
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        user = self.request.user

        direct_list = Network.objects.filter(
            referrer=user,
        )

        serializer = NetworkDirectListSerializer(
            direct_list,
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


class NetworkBinaryDetailAPIView(views.APIView):
    """
    API view to retrieve the binary network details for the authenticated user.

    This view handles a GET request to retrieve the binary network details for the authenticated user.

    Returns:
        - A JSON response containing the binary network details for the authenticated user:
            - Network Binary Details (object): Binary network details of the user represented as an object.
                - "status" (bool): true or false
                - "left_count" (int): Number of members in user's left side
                - "right_count" (int): Number of members in user's right side
                - "left_amount" (double): Amount of all invests in the user's left side
                - "right_amount" (double): Amount of all invests in the user's right side
                - "total_active_invest" (double): Amount of user's total active invest
                - "last_invest" (double): Amount of user's last active invest
                - "network_profit_daily_limit" (double): How much the user's profit wallet has been charged today
                - "network_profit" (double): How much the user has got from network, including direct and binary

    Note:
        - The API expects a GET request to retrieve the binary network details for the authenticated user.
        - The authenticated user is considered the account holder for whom the binary network details are retrieved.
        - The API queries the database for the binary network details of the user using the 'Network' model.
        - The serializer used to format the binary network details may vary based on the NetworkBinaryDetailSerializer used.
        - The binary network details provide information about the user's left and right subtree in the binary network.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": {
            "status": true,
            "left_count": 100,
            "right_count": 217,
            "left_amount": 1900.000,
            "right_amount": 2750.000,
            "total_active_invest": 750.000,
            "last_invest": 250.000,
            "network_profit_daily_limit": 0.000,
            "network_profit": 17500.000,
        },
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        user = self.request.user

        network_obj = Network.objects.get(
            user=user,
        )

        serializer = NetworkBinaryDetailSerializer(
            network_obj,
            context={"request": request},
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class NetworkDetailAPIView(views.APIView):
    """
    API view to retrieve the hierarchical network details for the authenticated user.

    This view handles a GET request to retrieve the hierarchical network details for the authenticated user.

    Returns:
        - A JSON response containing the hierarchical network details for the authenticated user:
            - Network Hierarchy (object): Hierarchical network details of the user represented as an object.
                - 'name' (str): The email of the user.
                - 'children' (list): A list of children nodes representing the user's left and right subtrees.
                    - Each child node contains:
                        - 'name' (str): The email of the child node.
                        - 'children' (list): A list of grandchildren nodes representing the next level in the hierarchy.

    Note:
        - The API expects a GET request to retrieve the hierarchical network details for the authenticated user.
        - The authenticated user's network hierarchy is represented as a binary tree structure.
        - The API queries the database for the network hierarchy of the user using the 'Network' model.
        - The hierarchical network details provide information about the user and their left and right subtrees.
        - The 'binary_place' field in the 'Network' model represents the binary position of the user in the network.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": {
            "name": "test@example.com",
            "children": [
                {
                    "name": "test1@example.com",
                    "children": [
                        {"name": "test11@example.com"},
                        {"name": "test12@example.com"},
                    ]
                },
                {
                    "name": "test2@example.com",
                    "children": [
                        {"name": "test21@example.com"},
                        {"name": "test22@example.com"},
                    ]
                }
            ]
        },
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        user = self.request.user

        try:
            network_obj = Network.objects.get(user=user)
        except Network.DoesNotExist:
            response = ApiResponse(
                success=False,
                code=404,
                error={
                    'code': 'network_not_found',
                    'detail': 'Network not found in the database',
                }
            )

            return Response(response)

        binary_place = network_obj.binary_place

        children_level1_left = Network.objects.filter(
            binary_place=binary_place + '0',
        ).first()

        children_level1_right = Network.objects.filter(
            binary_place=binary_place + '1',
        ).first()

        children_level2_left = list(
            Network.objects.filter(
                binary_place=binary_place + '00'
            ).values('user__email') | Network.objects.filter(
                binary_place=binary_place + '01'
            ).values('user__email')
        )

        children_level2_right = list(
            Network.objects.filter(
                binary_place=binary_place + '10'
            ).values('user__email') | Network.objects.filter(
                binary_place=binary_place + '11'
            ).values('user__email')
        )

        data = {
            'name': network_obj.user.email,
            'children': [
                {
                    'name': children_level1_left.user.email if children_level1_left else '',
                    'children': [{'name': child['user__email']} for child in children_level2_left]
                },
                {
                    'name': children_level1_right.user.email if children_level1_right else '',
                    'children': [{'name': child['user__email']} for child in children_level2_right]
                },
            ]
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)
