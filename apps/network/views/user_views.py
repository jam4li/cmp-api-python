from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.network.models import NetworkTransaction
from apps.network.serializers.user_serializers import NetworkTransactionListSerializer


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
