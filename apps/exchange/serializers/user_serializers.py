from rest_framework import serializers

from apps.exchange.models import ExchangeParent


class ParentDetailSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField(
        source='parent.user.email',
        read_only=True,
    )

    class Meta:
        model = ExchangeParent
        fields = [
            'parent',
            'status',
        ]
