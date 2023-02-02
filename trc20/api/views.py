from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext

from .serializers import Trc20CreateGatewaySerializer
from util.coinremitter import create_invoice

from trc20.models import Trc20


class Trc20CreateGatewayAPIView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        content = {
            'statusCode': '',
            'error': '',
            'message': '',
        }

        serializer = Trc20CreateGatewaySerializer(data=request.data)

        if serializer.is_valid():
            amount = self.request.data.get('amount')
            invoice = create_invoice(amount)

            serializer.save(
                invoice_id=invoice['data']['invoice_id'],
            )           

            return Response(invoice)

        else:
            content['statusCode'] = 400
            content['error'] = ''
            content['message'] = gettext('Not valid')

            return Response(content)
