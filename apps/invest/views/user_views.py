from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.invest.models import Invest
from apps.invest.serializers.user_serializers import InvestListSerializer


class InvestListAPIView(views.APIView):
    """
    API view to fetch a list of active investments for the authenticated user.

    This view handles a GET request to retrieve a list of active investments for the authenticated user.

    Returns:
        - A JSON response containing a list of active investments for the user:
            - Investment List (list): List of active investments, each represented as an object with investment details.
                - "id" (int): ID of instance
                - "package" (dict): Based on PackageInvestListSerializer
                - "invest" (double): The amount of investment
                - "profit" (double): How much profit the invest has until now

    Note:
        - The API expects a GET request to fetch a list of active investments for the authenticated user.
        - The authenticated user is considered the investor for whom the investment list is retrieved.
        - The API queries the database for investments that belong to the user and are not marked as 'finished'.
        - The investments are ordered by their creation date in ascending order.
        - The serializer used to format the investment list may vary based on the InvestListSerializer used.
        - The investment list provides information about each active investment, such as the investment amount, package details, etc.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "id": 1,
                "package": {
                    "id": 1,
                    "name": "5000$ Package",
                    "price": 5000.000,
                    "image": "https://image.com/img.jpg",
                },
                "invest": 5000.000,
                "profit": 100.000,
            },
            {
                "id": 2,
                "package": {
                    "id": 1,
                    "name": "5000$ Package",
                    "price": 5000.000,
                    "image": "https://image.com/img.jpg",
                },
                "invest": 5000.000,
                "profit": 177.000,
            },
            ...
        ],
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, *args, **kwargs):
        user = self.request.user

        invest_list = Invest.objects.filter(
            user=user,
            finished=False,
        ).order_by(
            'created_at',
        )

        serializer = InvestListSerializer(
            invest_list,
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
