from rest_framework import serializers

from wallet.models import Wallet

class WalletListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'title',
            'type',
            'access_type',
            'balance',
        ]
