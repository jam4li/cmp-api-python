from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.wallet.models import Wallet
from apps.wallet.serializers.user_serializers import WalletListSerializer


class WalletListAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        wallet = Wallet.objects.filter(
            user=user,
        )

        serializer = WalletListSerializer(
            wallet,
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
