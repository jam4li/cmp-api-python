from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.package.models import Package
from apps.package.serializers.user_serializers import PackageListSerializer


class PackageListAPIView(views.APIView):
    """
    API view to retrieve a list of active packages.

    This view handles a GET request to retrieve a list of active packages available in the system.

    Returns:
        - A JSON response containing the list of active packages:
            - Package List (list): A list of active package details represented as objects.
                - "id" (int): Id of the package
                - "name" (str): Name of the package
                - "price" (double): Price of the package, but user will pay price + fee
                - "image" (str): Image of the package
                - "summary" (str): A short summary of the package
                - "fee" (double): Fee of the package, user will pay price + fee
                - "daily_profit" (double): If the user buys this package, how much profit he will get everyday
                - "daily_profit_percent" (str): daily_profit= (daily_profit_percent * price) / 100
                - "profit_limit" (double): Limit of the profit

    Note:
        - The API expects a GET request to retrieve the list of active packages.
        - Active packages are filtered based on the 'status' field in the 'Package' model.
        - The packages are sorted by the 'sort' field to maintain a specific order, if provided.
        - The API queries the database for active packages using the 'Package' model.
        - The serializer used to format the package list may vary based on the PackageListSerializer used.

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "id": "1",
                "name": "100$ Package",
                "price": 100.000,
                "image": "https://image.com/image.jpg",
                "summary": "A good package",
                "fee": 17.5,
                "daily_profit": 1.7,
                "daily_profit_percent": 0.25,
            },
            {
                "id": "2",
                "name": "200$ Package",
                "price": 200.000,
                "image": "https://image.com/image.jpg",
                "summary": "A good package",
                "fee": 25,
                "daily_profit": 2.5,
                "daily_profit_percent": 0.2,
            },
        ],
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        package = Package.objects.filter(status=True).order_by('sort')

        serializer = PackageListSerializer(
            package,
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
