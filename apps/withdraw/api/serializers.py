from rest_framework import serializers

from apps.withdraw.models import Withdraw


class WithdrawListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = [
            'amount',
            'wallet_address',
            'transaction_hash',
            'status',
            'wallet_type',
            'updated_at',
        ]
