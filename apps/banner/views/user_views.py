from rest_framework import views
from rest_framework.response import Response

from apps.banner.models import Banner
from apps.banner.serializers.user_serializers import BannerListSerializer


class BannerListAPIView(views.APIView):
    def get(self, request, format=None):
        banners = Banner.objects.all().order_by(
            'sort',
        )

        serializer = BannerListSerializer(
            banners,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)
