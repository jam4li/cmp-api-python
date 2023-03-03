import requests
import hashlib
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK
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

            data = {
                'success': True,
                'data': {
                    'address': invoice['data']['url'],
                }
            }

            return Response(data)

        else:
            content['statusCode'] = 400
            content['error'] = ''
            content['message'] = gettext('Not valid')

            return Response(content)


class Trc20NotifyGatewayAPIView(views.APIView):
    def post(self, request, format=None):
        content = {
            'error': '',
        }

        try:
            status = self.request.data['status_code']

            if status == "1" or status == "2" or status == "3":
                invoice_id = self.request.data['invoice_id']
                amount = self.request.data['payment_history[0][amount]']
                transaction_hash = self.request.data['payment_history[0][txid]']
                symbol = 'USDT'

                payment = Trc20.objects.get(invoice_id=invoice_id)
                payment_code = payment.payment_code

                hash = str(payment_code) + str(transaction_hash) + "e178afd646065c77b36a5911448f7b41" + str(payment.user_id)
                hash = hash.encode()
                hash = hashlib.sha1(hash)
                hash = hash.hexdigest()

                body = {
                    'payment_code': payment_code,
                    'hash': hash,
                    'transaction_hash': transaction_hash,
                    'user_id': payment.user_id,
                    'amount': amount,
                    'symbol': symbol,
                }

                response = requests.post(payment.callback_url, data=body)

                return Response(body, status=HTTP_200_OK)

            else:
                return Response({}, status=HTTP_200_OK)

        except Exception as e:
            content['error'] = str(e)

            return Response(content, status=HTTP_200_OK)
