from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.banner.models import Banner
from apps.banner.serializers.user_serializers import BannerListSerializer


class BannerListAPIView(views.APIView):
    """
    API view to retrieve a list of published banners.

    This view handles a GET request to retrieve a list of banners that are in the 'publish' status.
    The banners are sorted by their 'publish_date' in ascending order.

    Returns:
        - A JSON response containing the list of published banners:
            - "title" (str): The title of the banner.
            - "author" (str): The author of the banner.
            - "image" (str): The URL of the banner image.
            - "summary" (str): The short summary about the banner.
            - "text" (str): The text that describes the banner.
            - "publish_date" (datetime): When the banner has been published.

    Note:
        - The API expects a GET request without any parameters.
        - The response contains a list of banners with the relevant details such as title, image URL,
          publish date, and status.
        - Banners are filtered by the 'publish' status and sorted by their 'publish_date' in ascending order.

    Example Request:
    ```
    GET /api/banners/
    ```

    Example Response:
    ```
    HTTP 200 OK
    {
        "success": true,
        "code": 200,
        "data": [
            {
                "title": "Banner 1",
                "author": "Admin",
                "image": "https://example.com/image.jpg",
                "summary": "A short summary",
                "text": "A short text about the banner",
                "publish_date": "2023-06-24"
            },
            {
                "title": "Banner 2",
                "author": "Admin",
                "image": "https://example.com/image.jpg",
                "summary": "A short summary",
                "text": "A short text about the banner",
                "publish_date": "2023-07-20"
            },
        ],
        "message": "Data retrieved successfully"
    }
    ```
    """

    def get(self, request, format=None):
        banners = Banner.objects.filter(
            status="publish",
        ).order_by(
            'publish_date',
        )

        serializer = BannerListSerializer(
            banners,
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
