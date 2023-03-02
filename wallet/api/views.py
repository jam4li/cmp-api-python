from rest_framework import views
from rest_framework.response import Response

from wallet.models import Wallet
from .serializers import WalletListSerializer


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

        return Response(serializer.data)
