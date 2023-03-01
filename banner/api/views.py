from rest_framework import views
from rest_framework.response import Response

from banner.models import Banner
from .serializers import BannerListSerializer


class BannerListAPIView(views.APIView):
    def get(self, request, format=None):
        banners = Banner.objects.all().order_by(
            'sort',
        )

        serializer = BannerListSerializer(banners, many=True)

        return Response(serializer.data)
