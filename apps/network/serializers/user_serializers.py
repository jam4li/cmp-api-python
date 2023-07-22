from rest_framework import serializers

from apps.network.models import Network, NetworkTransaction
from apps.users.models import User


class NetworkBinaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = [
            'status',
            'left_count',
            'right_count',
            'left_amount',
            'right_amount',
            'total_invest',
            'last_invest',
            'network_profit_daily_limit',
            'network_profit',
        ]


class NetworkUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
        ]


class NetworkDirectListSerializer(serializers.ModelSerializer):
    user = NetworkUserSerializer()

    class Meta:
        model = Network
        fields = [
            'user',
            'side',
        ]


class NetworkTransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkTransaction
        fields = [
            'type',
            'amount',
            'day',
            'description',
            'created_at',
        ]
