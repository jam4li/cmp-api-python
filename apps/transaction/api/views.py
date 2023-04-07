from rest_framework import views
from rest_framework.response import Response

from apps.transaction.models import Transaction
from .serializers import TransactionListSerializer


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

        return Response(serializer.data)
