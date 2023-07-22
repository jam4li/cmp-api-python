from django.conf import settings
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from utils.response import ApiResponse
from apps.users.utils.google_auth import create_google_url, callback_google
from apps.users.utils.register import create_user

from apps.users.models import User, UserProfile
from apps.invest.models import Invest
from apps.wallet.models import Wallet
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
            if wallet.type == 'eit':
                balance += (wallet.balance // 4)
            else:
                balance += wallet.balance

        direct_invited = Network.objects.filter(
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
        user = self.request.user
        email = user.email.split('@')[0]
        data = {
            "email": email,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class UserCreateAPIView(views.APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        referrer_referrer_code = self.request.data['referrer']
        side = self.request.data['side']

        try:
            referrer_profile = UserProfile.objects.get(
                referrer_code=referrer_referrer_code,
            )
        except UserProfile.DoesNotExist:
            response = ApiResponse(
                success=False,
                code=404,
                error={
                    'code': 'referrer_not_found',
                    'detail': 'Referrer user not found in the database',
                }
            )
            return Response(response)

        # Create gmail login link

        url = create_google_url(
            side=side,
            referrer_code=referrer_referrer_code,
        )

        # Create new user's profile

        return Response({'url': url})


class UserReferralDetailAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)

        data = {
            "referrer_code": user_profile.referrer_code,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class GoogleLogin(views.APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        url = create_google_url()
        return Response({'url': url})


class GoogleCallback(views.APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        id_info = callback_google(request)

        user_email = id_info['email']
        user_name = id_info['name']

        user_side = id_info['side']
        user_referrer_code = id_info['referrer_code']

        if user_side and user_referrer_code:
            create_user(
                email=user_email,
                side=user_side,
                referrer_code=user_referrer_code,
            )

        user = User.objects.get(email=user_email)
        token, created = Token.objects.get_or_create(user=user)

        front_end_url = settings.FRONT_END_URL

        redirect_url = front_end_url + "/dashboard/?token={0}&email={1}".format(
            token,
            user_email,
        )

        return redirect(redirect_url)


class Logout(views.APIView):
    def get(self, request):
        try:
            Token.objects.get(user=request.user).delete()
        except User.DoesNotExist:
            return Response({"Error:": f"Could not find user with email:{request.user.email}"}, status=status.HTTP_400_BAD_REQUEST)
