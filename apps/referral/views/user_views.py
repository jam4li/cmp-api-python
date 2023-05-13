from rest_framework import views, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from utils.response import ApiResponse

from apps.referral.models import Referral
from apps.network.models import Network
from apps.referral.serializers.user_serializers import ReferralDirectListSerializer, ReferralBinaryDetailSerializer

from apps.referral.tasks import my_example_task


class ReferralDirectListAPIView(views.APIView):
    def get(self, request, format=None):
        my_example_task.apply_async()
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


class ReferralNetworkDetailAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            referral_obj = Referral.objects.get(user=user)
        except Referral.DoesNotExist:
            response = ApiResponse(
                success=False,
                code=404,
                error={
                    'code': 'referral_not_found',
                    'detail': 'Referral not found in the database',
                }
            )

            return Response(response)

        binary_place = referral_obj.binary_place

        children_level1_left = Referral.objects.filter(
            binary_place=binary_place + '0',
        ).first()

        children_level1_right = Referral.objects.filter(
            binary_place=binary_place + '1',
        ).first()

        children_level2_left = list(
            Referral.objects.filter(
                binary_place=binary_place + '00').values('user__email') | Referral.objects.filter(binary_place=binary_place + '01').values('user__email')
        )

        children_level2_right = list(
            Referral.objects.filter(binary_place=binary_place + '10').values(
                'user__email') | Referral.objects.filter(binary_place=binary_place + '11').values('user__email')
        )

        data = {
            'name': referral_obj.user.email,
            'children': [
                {
                    'name': children_level1_left.user.email if children_level1_left else '',
                    'children': [{'name': child['user__email']} for child in children_level2_left]
                },
                {
                    'name': children_level1_right.user.email if children_level1_right else '',
                    'children': [{'name': child['user__email']} for child in children_level2_right]
                },
            ]
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)
