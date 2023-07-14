from django.utils import timezone

from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.withdraw.models import Withdraw
from apps.wallet.models import Wallet

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

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class WithdrawDetailAPIView(views.APIView):
    def get(self, request, format=None):
        wallet_types = [
            {
                'wallet_type': choice[0],
                'display_name': choice[1]
            }
            for choice in Withdraw.WALLET_TYPE_CHOICES
        ]

        data = {
            'wallet_types': wallet_types,
            'is_active': True,
        }

        success_response = ApiResponse(
            success=True,
            code=200,
            data=data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class WithdrawCreateAPIView(views.APIView):
    def post(self, request, format=None):
        user = self.request.user
        wallet_address = self.request.data['wallet_address']
        wallet_type = self.request.data['wallet_type']
        amount = self.request.data['amount']

        amount = float(amount)

        # Calculate fee
        fee = 0

        if wallet_type == 'commission':
            fee = (10 * amount) / 100

        elif wallet_type == 'profit':
            fee = 2

        # Check wallet balance based on the wallet_type
        wallet = Wallet.objects.get(
            user=user,
            type=wallet_type,
        )

        wallet_balance = float(wallet.balance)

        if fee > amount:
            response = ApiResponse(
                success=False,
                code=402,
                error={
                    'code': 'fee greater than_amount',
                    'detail': 'Fee cannot be greater than the amount.',
                }
            )

            return Response(response)

        if wallet_balance < amount:
            response = ApiResponse(
                success=False,
                code=402,
                error={
                    'code': 'insufficient balance',
                    'detail': 'Insufficient balance in wallet',
                }
            )

            return Response(response)

        Withdraw.objects.create(
            user=user,
            amount=amount - fee,
            fee=fee,
            wallet_address=wallet_address,
            wallet_type=wallet_type,
            status='pending',
            created_at=timezone.now(),
        )

        wallet.balance = wallet_balance - (amount)
        wallet.updated_at = timezone.now()
        wallet.save()

        success_response = ApiResponse(
            success=True,
            code=200,
            message='Data retrieved successfully'
        )

        return Response(success_response)
