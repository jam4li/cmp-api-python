from rest_framework import serializers

from apps.invest.models import Invest
from apps.package.models import Package
from apps.users.models import User


class PackageInvestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            'id',
            'name',
            'price',
            'image',
        ]


class InvestListSerializer(serializers.ModelSerializer):
    package = PackageInvestListSerializer(read_only=True)

    class Meta:
        model = Invest
        fields = [
            'id',
            'package',
            'invest',
            'profit',
        ]
