from rest_framework import views
from rest_framework.response import Response

from invest.models import Invest
from config.models import Config
from .serializers import InvestListSerializer


class InvestListAPIView(views.APIView):
    def get(self, request, status=None, *args, **kwargs):
        if status == 'all' or status == 'finished' or status == 'active':
            invest_list = Invest.objects.all()
            serializer = InvestListSerializer(
                invest_list,
                many=True,
                context={"request": request},
            )

            personal_limit_percent = Config.objects.get(key='personal_limit_percent')

            data = {
                "invests": serializer.data,
                "personal_limit_percent": personal_limit_percent.value,
            }

            return Response(data)
