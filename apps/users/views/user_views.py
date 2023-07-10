from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.users.models import User
from apps.invest.models import Invest
from apps.wallet.models import Wallet
from apps.referral.models import Referral
from apps.network.models import Network
# from .serializers import BannerListSerializer


class UserDashboardAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        # Calculate active packages
        active_packages = Invest.objects.filter(
            user=user,
            finished=False,
        ).count()

        # Calculate balance
        balance = 0
        wallet_list = Wallet.objects.filter(user=user)
        for wallet in wallet_list:
            if wallet.type == 'cmp':
                balance += (wallet.balance // 4)
            else:
                balance += wallet.balance

        direct_invited = Referral.objects.filter(
            referrer=user,
        ).count()

        user_network = Network.objects.get(user=user)
        binary_right_count = user_network.right_count
        binary_left_count = user_network.left_count
        team = binary_right_count + binary_left_count

        data = {
            "active_packages": active_packages,
            "balance": balance,
            "direct_invited": direct_invited,
            "team": team,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class UserDetailAPIView(views.APIView):
    def get(self, request, format=None):
        data = {
            "name": "User",
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)
