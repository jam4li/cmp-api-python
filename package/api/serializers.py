from rest_framework import serializers

from package.models import Package

class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            'name',
            'price',
            'image',
            'summery',
            'fee',
            'daily_profit',
            'daily_profit_percent',
            'profit_limit',
        ]
