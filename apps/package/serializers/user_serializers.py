from rest_framework import serializers

from apps.package.models import Package


class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            'id',
            'name',
            'price',
            'image',
            'summary',
            'fee',
            'daily_profit',
            'daily_profit_percent',
            'profit_limit',
        ]
