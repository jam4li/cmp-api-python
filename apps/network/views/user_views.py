from django.utils.translation import gettext_lazy as _
from rest_framework import views, status
from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.network.models import Network, NetworkTransaction
from apps.network.serializers.user_serializers import (
    NetworkBinaryDetailSerializer,
    NetworkDirectListSerializer,
    NetworkTransactionListSerializer,
)


class NetworkTransactionListAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        network_transaction_list = NetworkTransaction.objects.filter(
            user=user,
        ).order_by(
            '-id',
        )

        serializer = NetworkTransactionListSerializer(
            network_transaction_list,
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


class NetworkDirectListAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        direct_list = Network.objects.filter(
            referrer=user,
        )

        serializer = NetworkDirectListSerializer(
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


class NetworkBinaryDetailAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        network_obj = Network.objects.get(
            user=user,
        )

        serializer = NetworkBinaryDetailSerializer(
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


class NetworkDetailAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            network_obj = Network.objects.get(user=user)
        except Network.DoesNotExist:
            response = ApiResponse(
                success=False,
                code=404,
                error={
                    'code': 'network_not_found',
                    'detail': 'Network not found in the database',
                }
            )

            return Response(response)

        binary_place = network_obj.binary_place

        children_level1_left = Network.objects.filter(
            binary_place=binary_place + '0',
        ).first()

        children_level1_right = Network.objects.filter(
            binary_place=binary_place + '1',
        ).first()

        children_level2_left = list(
            Network.objects.filter(
                binary_place=binary_place + '00'
            ).values('user__email') | Network.objects.filter(
                binary_place=binary_place + '01'
            ).values('user__email')
        )

        children_level2_right = list(
            Network.objects.filter(
                binary_place=binary_place + '10'
            ).values('user__email') | Network.objects.filter(
                binary_place=binary_place + '11'
            ).values('user__email')
        )

        data = {
            'name': network_obj.user.email,
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
