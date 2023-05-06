from rest_framework import views
from rest_framework.response import Response
from django.utils.translation import gettext

from utils.response import ApiResponse

from apps.trc20.serializers.user_serializers import Trc20CreateGatewaySerializer
from apps.trc20.models import Trc20

from utils.coinremitter import create_invoice


class Trc20CreateGatewayAPIView(views.APIView):
    def post(self, request, format=None):
        serializer = Trc20CreateGatewaySerializer(data=request.data)

        if serializer.is_valid():
            total_amount = self.request.data.get('total_amount')
            invoice = create_invoice(total_amount)

            invoice_message = invoice['msg']
            invoice_data = invoice['data']

            serializer.save(
                user=self.request.user,
                message=invoice_message,
                invoice_id=invoice_data['invoice_id'],
                total_amount=float(
                    invoice_data['total_amount']['USDTTRC20'],
                ),
                address=invoice_data['address'],
                symbol=invoice_data['coin'],
                status=invoice_data['status_code'],
            )

            data = {
                'gateway_address': invoice['data']['url'],
            }

            success_response = ApiResponse(
                success=True,
                code=200,
                data=data,
                message='Data retrieved successfully'
            )

            return Response(success_response)

        else:
            response = ApiResponse(
                success=False,
                code=400,
                error={
                    'code': 'not_valid',
                    'detail': 'Not valid',
                }
            )

            return Response(response)


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

                hash = str(payment_code) + str(transaction_hash) + \
                    "e178afd646065c77b36a5911448f7b41" + str(payment.user_id)
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
