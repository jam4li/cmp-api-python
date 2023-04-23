from rest_framework import views, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from utils.response import ApiResponse

from apps.referral.models import Referral
from apps.network.models import Network
from apps.referral.serializers.user_serializers import ReferralDirectListSerializer, ReferralBinaryDetailSerializer


class ReferralDirectListAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        direct_list = Referral.objects.filter(
            referrer=user,
        )

        serializer = ReferralDirectListSerializer(
            direct_list,
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


class ReferralBinaryDetailAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        network_obj = Network.objects.get(
            user=user,
        )

        serializer = ReferralBinaryDetailSerializer(
            network_obj,
            context={"request": request},
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)
