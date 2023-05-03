from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.banner.models import Banner
from apps.banner.serializers.user_serializers import BannerListSerializer


class BannerListAPIView(views.APIView):
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
