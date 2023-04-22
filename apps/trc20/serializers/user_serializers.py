from rest_framework import serializers

from apps.trc20.models import Trc20


class Trc20CreateGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Trc20
        fields = (
            'amount',
            'payment_code',
            'user_id',
            'symbol',
            'callback_url',
        )
