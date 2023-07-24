from rest_framework import views, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from utils.response import ApiResponse

from apps.support.models import SupportDepartment, SupportTicket, SupportTicketReply
from apps.support.serializers.user_serializers import SupportDepartmentListSerializer, SupportTicketCreateSerializer, SupportTicketListSerializer, SupportTicketDetailSerializer


class SupportDepartmentListAPIView(views.APIView):
    """
    API view to fetch a list of support departments.

    This view handles a GET request to retrieve a list of support departments.

    Returns:
        - A JSON response containing a list of support departments:
            - Support Department List (list): List of support departments, each represented as an object with department details.
                - "id" (int): Id of the department list
                - "name" (str): (e.g., "Withdraw")
                - "icon" (str): (e.g., "https://icon.com/icon.png")
                - "is_active" (bool): The department is active or not. True or False.

    Note:
        - The API expects a GET request to fetch a list of support departments.
        - The API queries the database to retrieve all support departments available.
        - The serializer used to format the support department list may vary based on the SupportDepartmentListSerializer used.
        - The support department list provides information about each department, such as the department name, contact details, etc.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "id": 1,
                "name": "Withdraw",
                "icon": "https://icon.com/icon.png",
                "is_active": true,
            },
            {
                "id": 2,
                "name": "Technical Support",
                "icon": "https://icon.com/icon.png",
                "is_active": true,
            },
        ],
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        support_department = SupportDepartment.objects.all()
        serializer = SupportDepartmentListSerializer(
            support_department,
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


class SupportTicketCreateAPIView(views.APIView):
    """
    API view to create a support ticket for the authenticated user.

    This view handles a POST request to create a support ticket for the authenticated user.

    Parameters (in the POST request body):
        - "department" (int): Id of the ticket department
        - "title" (str): The title that user fills
        - "content" (str): The content that user fills

    Returns:
        - A JSON response confirming the successful creation of the support ticket:
            - "success" (bool): A boolean flag indicating the success of the ticket creation (True) or failure (False).
            - "message" (str): A message indicating the status of the support ticket creation.
            - "ticket_id" (int): The unique identifier of the created support ticket.

    Note:
        - The API expects a POST request with the required parameters to create a support ticket for the authenticated user.
        - The authenticated user is considered the account holder who initiates the support ticket.
        - Before creating a support ticket, the API checks if the user already has an open support ticket.
        - If the user has an open support ticket, the API returns an error response indicating that a new ticket cannot be created.
        - The serializer used validates the request data for creating the support ticket.
        - If the request data is valid, a SupportTicket object is created in the database with the provided details.
        - The response confirms the success or failure of the support ticket creation and includes the ticket_id if successful.

    Example Response (Success):
    ```
    HTTP 201 CREATED
    {
        "success": true,
        "message": "Support ticket created successfully.",
        "ticket_id": 1234
    }
    ```

    Example Response (Failure):
    ```
    HTTP 400 BAD REQUEST
    {
        "success": false,
        "message": "Failed to create support ticket.",
        "errors": {
            "error": ["Error message 1", "Error message 2", ...],
        }
    }
    ```
    """

    def post(self, request):
        user = self.request.user

        has_support_ticket = SupportTicket.objects.filter(
            user=user,
            status="open",
        ).exists()

        if has_support_ticket:
            return Response({
                "success": False,
                "message": _("Failed to create support ticket."),
                "errors": serializer.errors,
            },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SupportTicketCreateSerializer(
            data=request.data,
            context={'request': request},
        )

        if serializer.is_valid(raise_exception=True):
            support_ticket = serializer.save(
                user=user,
            )

            return Response({
                "success": True,
                "message": _("Support ticket created successfully."),
                "ticket_id": support_ticket.id,
            },
                status=status.HTTP_201_CREATED,
            )

        return Response({
            "success": False,
            "message": _("Failed to create support ticket."),
            "errors": serializer.errors,
        },
            status=status.HTTP_400_BAD_REQUEST,
        )


class SupportTicketListAPIView(views.APIView):
    """
    API view to fetch a list of support tickets for the authenticated user.

    This view handles a GET request to retrieve a list of support tickets for the authenticated user.

    Returns:
        - A JSON response containing a list of support tickets for the user:
            - Support Ticket List (list): List of support tickets, each represented as an object with ticket details.
                - "id" (int): Id of the ticket
                - "content" (str): Content of the ticket
                - "created_at" (datetime): When the ticket has been created

    Note:
        - The API expects a GET request to fetch a list of support tickets for the authenticated user.
        - The authenticated user is considered the account holder for whom the support tickets are retrieved.
        - The API queries the database for support tickets that belong to the user.
        - The serializer used to format the support ticket list may vary based on the SupportTicketListSerializer used.
        - The support ticket list provides information about each ticket, such as the ticket status, subject, etc.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "id": 1,
                "title": "Issue with login",
                "content": "When I want to login it redirects to yahoo.com",
                "created_at": "2023-07-22",
            },
            {
                "id": 2,
                "title": "Withdraw",
                "content": "When the profit will be sent to my wallet",
                "created_at": "2023-07-23",
            },
        ],
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        user = self.request.user

        support_ticket = SupportTicket.objects.filter(user=user)

        serializer = SupportTicketListSerializer(
            support_ticket,
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


class SupportTicketDetailAPIView(views.APIView):
    """
    API view to fetch and post replies for a specific support ticket.

    This view handles GET and POST requests related to a specific support ticket.

    Parameters:
        - "pk" (int): The primary key of the support ticket to retrieve or reply to.

    Returns:
        - For GET request:
            - A JSON response containing a list of replies for the specified support ticket:
                - Support Ticket Reply List (list): List of replies, each represented as an object with reply details.
                    - "content" (str): The content of the reply

        - For POST request:
            - A JSON response confirming the successful creation of the reply:
                - "success" (bool): A boolean flag indicating the success of the reply creation (True) or failure (False).
                - "message" (str): A message indicating the status of the reply creation.

    Note:
        - The API expects a GET request with the 'pk' parameter to fetch replies for a specific support ticket.
        - The API expects a POST request with the 'pk' parameter and a 'reply' parameter to create a reply for the ticket.
        - The 'pk' parameter represents the unique identifier (primary key) of the support ticket.
        - If the specified support ticket with the given 'pk' does not exist, the API returns an empty response for both GET and POST.
        - For the GET request, the API fetches all the replies related to the specified support ticket from the database.
        - The serializer used to format the support ticket reply list may vary based on the SupportTicketDetailSerializer used.
        - For the POST request, the API updates the support ticket with the new reply and creates a SupportTicketReply object in the database.
        - The response for the POST request confirms the success or failure of the reply creation.

    Example Response (GET):
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "content": "Thank you for contacting us.",
            },
            {
                "content": "We apologize for the inconvenience.",
            },
        ],
        "message": "Data retrieved successfully"
    }
    ```

    Example Response (POST - Success):
    ```
    HTTP 200 OK
    {
        "success": true,
        "message": "Data created successfully"
    }
    ```

    Example Response (POST - Failure):
    ```
    HTTP 400 BAD REQUEST
    {
        "success": false,
        "message": "Failed to create reply. Please check your request data."
    }
    ```
    """

    def get(self, request, pk, format=None):
        try:
            support_ticket = SupportTicket.objects.get(id=pk)
        except SupportTicket.DoesNotExist:
            pass

        support_ticket_reply_list = SupportTicketReply.objects.filter(
            ticket=support_ticket,
        )

        serializer = SupportTicketDetailSerializer(
            support_ticket_reply_list,
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

    def post(self, request, pk, format=None):
        try:
            support_ticket = SupportTicket.objects.get(id=pk)
        except SupportTicket.DoesNotExist:
            pass

        reply = self.request.data.get('reply')

        support_ticket.is_admin_replied = False
        support_ticket.save()

        SupportTicketReply.objects.create(
            ticket=support_ticket,
            content=reply,
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data={},
            message='Data created successfully'
        )

        return Response(success_response)
