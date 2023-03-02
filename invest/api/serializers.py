from rest_framework import serializers

from invest.models import Invest
from package.models import Package
from users.models import User


class PackageInvestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            'id',
            'name',
            'price',
            'image',
        ]


class UserInvestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
        ]


class InvestListSerializer(serializers.ModelSerializer):
    package = PackageInvestListSerializer(read_only=True)
    user = UserInvestListSerializer(read_only=True)

    class Meta:
        model = Invest
        fields = [
            'package',
            'user',
            'invest',
            'total_invest',
            'profit',
            'payout_binary_status',
            'payout_direct_status',
            'finished',
        ]
