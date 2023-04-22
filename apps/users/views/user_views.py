from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.users.models import User
from apps.invest.models import Invest
from apps.wallet.models import Wallet
# from .serializers import AnnouncementListSerializer


class UserDashboardAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        # Calculate active packages
        active_packages = Invest.objects.filter(user=user).count()

        # Calculate balance
        balance = 0
        wallet_list = Wallet.objects.filter(user=user)
        for wallet in wallet_list:
            balance += wallet.balance

        data = {
            "active_packages": active_packages,
            "balance": balance,
            "direct_invited": "Pending",
            "team": "Pending",
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
