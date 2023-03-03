from rest_framework import views
from rest_framework.response import Response

from package.models import Package
from .serializers import PackageListSerializer, PackageBuySerializer


class PackageListAPIView(views.APIView):
    def get(self, request, format=None):
        package = Package.objects.filter(status=True)

        serializer = PackageListSerializer(
            package,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)


class PackageBuyAPIView(views.APIView):
    def post(self, request, format=None):
        serializer = PackageBuySerializer(data=self.request.data)

        if serializer.is_valid():
            package_id = serializer.data['id']
            symbol = serializer.data['symbol']

            # Check if package exists or not
            try:
                package = Package.objects.get(id=package_id)

            except Package.DoesNotExist:
                return Response({'Not found'})

            if symbol == 'USDT':
                amount = package.price + package.fee

                # TODO: Call validate_deposit_and_voucher_amount
                # TODO: Call transfer_deposit_and_voucher_amount_to_company_wallet

            return Response(serializer.data)
