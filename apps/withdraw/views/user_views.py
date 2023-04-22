from rest_framework import views
from rest_framework.response import Response

from apps.withdraw.models import Withdraw
from apps.withdraw.serializers.user_serializers import WithdrawListSerializer


class WithdrawListAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        withdraw_list = Withdraw.objects.filter(
            user=user,
        ).order_by(
            'created_at',
        )

        serializer = WithdrawListSerializer(
            withdraw_list,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)
