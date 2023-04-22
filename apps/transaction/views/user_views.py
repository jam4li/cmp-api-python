from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.transaction.models import Transaction
from apps.transaction.serializers.user_serializers import TransactionListSerializer


class TransactionListAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        transaction_list = Transaction.objects.filter(
            user=user,
        ).order_by(
            'created_at',
        )

        serializer = TransactionListSerializer(
            transaction_list,
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
