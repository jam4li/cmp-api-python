from rest_framework import serializers

from apps.network.models import NetworkTransaction


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
