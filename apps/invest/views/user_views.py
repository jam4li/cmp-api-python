from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.invest.models import Invest
from apps.invest.serializers.user_serializers import InvestListSerializer


class InvestListAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user

        invest_list = Invest.objects.filter(
            user=user,
            finished=False,
        ).order_by(
            'created_at',
        )

        serializer = InvestListSerializer(
            invest_list,
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
