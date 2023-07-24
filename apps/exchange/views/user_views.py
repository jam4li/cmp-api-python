from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from utils.response import ApiResponse

from apps.users.models import User
from apps.exchange.models import ExchangeParent

from apps.exchange.serializers.user_serializers import ParentDetailSerializer, CMEXBITExchangeParentSeiralizer


class CMEXBITApiView(views.APIView):
    """
    API view to fetch CMEXBIT exchange parent information.

    This view handles a POST request to retrieve CMEXBIT exchange parent information based on the provided email.

    Parameters:
        - 'email' (str): The email of the user for whom the CMEXBIT exchange parent information is requested.

    Returns:
        - A JSON response containing CMEXBIT exchange parent information:
            - Exchange Parent Data (varies based on serializer):
                - "user" (dict): Based on CMEXBITUserSerializer
                - "parent" (dict): Based on CMEXBITUserSerializer
                - "status" (str): rejected, accepted, pending

    Note:
        - The API expects a POST request with the 'email' parameter to identify the user.
        - The API retrieves the user based on the provided email.
        - If the user is not found in the database, an error response is returned with a 404 status code.
        - If the user is found but has no associated exchange parent, another error response is returned with a 404 status code.
        - If the user and the associated exchange parent are found, the exchange parent data is serialized and returned in the response.
        - The serializer used to format the exchange parent data may vary based on the CMEXBITExchangeParentSeiralizer used.

    Example Response (Success):
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": {
            "user": {
                "email": "user@gmail.com",
                "name": "user",
            },
            "parent": {
                "email": "parent@gmail.com",
                "name": "parent",
            },
            status: "pending",
        },
        "message": "Data retrieved successfully"
    }
    ```

    Example Response (User Not Found):
    ```
    HTTP 404 NOT FOUND
    {
        "success": false,
        "code": 404,
        "error": {
            "code": "user_not_found",
            "detail": "User not found in the database"
        }
    }
    ```

    Example Response (Parent Not Found):
    ```
    HTTP 404 NOT FOUND
    {
        "success": false,
        "code": 404,
        "error": {
            "code": "parent_not_found",
            "detail": "The parent email not found"
        }
    }
    ```
    """
    permission_classes = [AllowAny, ]

    def post(self, request):
        email = self.request.data.get('email')

        try:
            user = User.objects.get(email=email)
            exchange_parent = ExchangeParent.objects.get(user=user)

        except User.DoesNotExist:
            response = ApiResponse(
                success=False,
                code=404,
                error={
                    'code': 'user_not_found',
                    'detail': 'User not found in the database',
                }
            )

            return Response(response)

        except ExchangeParent.DoesNotExist:
            response = ApiResponse(
                success=False,
                code=404,
                error={
                    'code': 'parent_not_found',
                    'detail': 'The parent email not found',
                }
            )

            return Response(response)

        serializer = CMEXBITExchangeParentSeiralizer(exchange_parent)

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class ParentCreateAPIView(views.APIView):
    """
    API view to create a parent-child relationship between users for exchange purposes.

    This view handles a POST request to create a parent-child relationship between two users for exchange purposes.

    Parameters:
        - 'parent_email' (str): The email of the parent user to establish the relationship.

    Returns:
        - A JSON response containing information about the exchange parent:
            - "exchange_parent" (str): The identifier (e.g., ExchangeParent object representation) of the exchange parent.

    Note:
        - The API expects a POST request with the 'parent_email' parameter to identify the parent user.
        - The authenticated user is considered the child user in the parent-child relationship.
        - The API retrieves the parent user based on the provided email.
        - If the parent user is not found in the database, a TODO comment indicates that a User.DoesNotExist handler needs to be added.
        - If the parent user is found, a parent-child relationship is created for exchange purposes.
        - The child user's exchange parent field is set to the parent user's ExchangeParent object.
        - If the child user already has an exchange parent, it will be replaced with the new one.
        - The identifier (e.g., object representation) of the exchange parent is returned in the response.

    Example Response:
    ```
    HTTP 200 OK
    {
        "exchange_parent": "parent@gmail.com"
    }
    ```
    """

    def post(self, request):
        user = self.request.user

        parent_email = self.request.data.get('parent_email')

        # TODO: Add User.DoesnotExist handler
        parent_user = User.objects.get(email=parent_email)

        exchange_parent = ExchangeParent.objects.get(
            user=parent_user,
        )

        exchange_children, _ = ExchangeParent.objects.get_or_create(
            user=user,
        )

        exchange_children.parent = exchange_parent
        exchange_children.save()

        data = {
            'exchange_parent': str(exchange_children.parent),
        }

        return Response(data)


class ParentDetailAPIView(views.APIView):
    """
    API view to fetch exchange parent details for the authenticated user.

    This view handles a GET request to retrieve the exchange parent details of the authenticated user.

    Returns:
        - A JSON response containing exchange parent details for the user:
            - Exchange Parent Data:
                - "parent" (str): The email of the user's parent
                - "status" (str): rejected, accepted, pending
                - "accepted_users": Based on ExchangeUserSerializer
                - "rejected_users": Based on ExchangeUserSerializer
                - "pending_users": Based on ExchangeUserSerializer

    Note:
        - The API expects a GET request to fetch exchange parent details of the authenticated user.
        - The authenticated user is considered the child user in the parent-child relationship.
        - The API retrieves the exchange parent details based on the authenticated user.
        - If the authenticated user has an associated exchange parent, the details are serialized and returned in the response.
        - The serializer used to format the exchange parent details may vary based on the ParentDetailSerializer used.
        - If the authenticated user does not have an associated exchange parent, an empty response is returned with a 200 status code.

    Example Response (Exchange Parent Exists):
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": {
            "parent": "parent@gmail.com",
            "status": "accepted",
            "accepted_users": [
                {
                    "email": "accepted@gmail.com",
                    "accept_url" : "https://accept.com",
                    "reject_url" : "https://reject.com",
                }
            ],
            "rejected_users": [
                {
                    "email": "accepted@gmail.com",
                    "accept_url" : "https://accept.com",
                    "reject_url" : "https://reject.com",
                }
            ],
            "pending_users": [
                {
                    "email": "accepted@gmail.com",
                    "accept_url" : "https://accept.com",
                    "reject_url" : "https://reject.com",
                }
            ],
        },
        "message": "Data retrieved successfully"
    }
    ```

    Example Response (Exchange Parent Not Found):
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": {},
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        user = self.request.user

        try:
            exchange_parent = ExchangeParent.objects.get(user=user)

            serializer = ParentDetailSerializer(
                exchange_parent,
                context={"request": request},
            )

            success_response = ApiResponse(
                success=True,
                code=200,
                data=serializer.data,
                message='Data retrieved successfully'
            )

            return Response(success_response)

        except ExchangeParent.DoesNotExist:
            success_response = ApiResponse(
                success=True,
                code=200,
                data={},
                message='Data retrieved successfully'
            )

            return Response(success_response)


class AcceptUserView(views.APIView):
    """
    API view to accept a user as an exchange child.

    This view handles a GET request to accept a user as an exchange child based on the provided user_id.

    Parameters:
        - 'user_id' (int): The unique identifier of the user to be accepted as an exchange child.

    Returns:
        - A JSON response confirming the user acceptance as an exchange child:
            - "status" (str): A status message indicating that the user has been accepted.

    Note:
        - The API expects a GET request with the 'user_id' parameter to identify the user to be accepted as an exchange child.
        - The authenticated user performs this action.
        - The API retrieves the user based on the provided user_id.
        - If the user is found, the associated ExchangeParent object is updated to 'accepted' status.
        - The 'accepted' status indicates that the user has been accepted as an exchange child.
        - If the user_id does not correspond to any existing user, a User.DoesNotExist exception is raised.

    Example Response:
    ```
    HTTP 200 OK
    {
        "status": "Accepted"
    }
    ```
    """

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(
            id=user_id,
        )

        exchange_parent = ExchangeParent.objects.get(
            user=user,
        )
        exchange_parent.status = 'accepted'
        exchange_parent.save()

        return Response({'status': 'Accepted'})


class RejectUserView(views.APIView):
    """
    API view to reject a user as an exchange child.

    This view handles a GET request to reject a user as an exchange child based on the provided user_id.

    Parameters:
        - 'user_id' (int): The unique identifier of the user to be rejected as an exchange child.

    Returns:
        - A JSON response confirming the user rejection as an exchange child:
            - "status" (str): A status message indicating that the user has been rejected.

    Note:
        - The API expects a GET request with the 'user_id' parameter to identify the user to be rejected as an exchange parent.
        - The authenticated user (presumably an admin or authorized user) performs this action.
        - The API retrieves the user based on the provided user_id.
        - If the user is found, the associated ExchangeParent object is updated to 'rejected' status.
        - The 'rejected' status indicates that the user has been rejected as an exchange child.
        - If the user_id does not correspond to any existing user, a User.DoesNotExist exception is raised.

    Example Response:
    ```
    HTTP 200 OK
    {
        "status": "Rejected"
    }
    ```
    """

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(
            id=user_id,
        )

        exchange_parent = ExchangeParent.objects.get(
            user=user,
        )
        exchange_parent.status = 'rejected'
        exchange_parent.save()

        return Response({'status': 'Rejected'})
