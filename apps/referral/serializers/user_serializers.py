from rest_framework import serializers

from apps.referral.models import Referral
from apps.network.models import Network
from apps.users.models import User


class ReferralUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
        ]


class ReferralDirectListSerializer(serializers.ModelSerializer):
    user = ReferralUserSerializer()

    class Meta:
        model = Referral
        fields = [
            'user',
        ]


class ReferralBinaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = [
            'left_count',
            'right_count',
            'left_amount',
            'right_amount',
        ]
