from rest_framework import serializers

from package.models import Package


class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            'id',
            'name',
            'price',
            'image',
            'summery',
            'fee',
            'daily_profit',
            'daily_profit_percent',
            'profit_limit',
        ]


class PackageBuySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    symbol = serializers.CharField(max_length=10)
    voucher_amount = serializers.IntegerField(allow_null=True)
