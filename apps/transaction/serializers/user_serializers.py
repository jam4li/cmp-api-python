from rest_framework import serializers

from apps.transaction.models import Transaction


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'type',
            'description',
            'updated_at',
        ]
