from rest_framework import views
from rest_framework.response import Response

from package.models import Package
from .serializers import PackageListSerializer


class PackageListAPIView(views.APIView):
    def get(self, request, format=None):
        package = Package.objects.filter(status=True)

        serializer = PackageListSerializer(
            package,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)
