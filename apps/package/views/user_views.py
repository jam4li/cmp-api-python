from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.package.models import Package
from apps.package.serializers.user_serializers import PackageListSerializer


class PackageListAPIView(views.APIView):
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
