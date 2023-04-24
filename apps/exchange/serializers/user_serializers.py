from rest_framework import serializers
from django.urls import reverse

from apps.exchange.models import ExchangeParent
from apps.users.models import User


class ExchangeUserSerializer(serializers.ModelSerializer):
    accept_url = serializers.SerializerMethodField()
    reject_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'accept_url',
            'reject_url',
        ]

    def get_accept_url(self, obj):
        request = self.context.get('request')
        relative_url = reverse(
            'exchange_user:accept-user',
            kwargs={'user_id': obj.id},
        )
        return request.build_absolute_uri(relative_url)

    def get_reject_url(self, obj):
        request = self.context.get('request')
        relative_url = reverse(
            'exchange_user:reject-user',
            kwargs={'user_id': obj.id},
        )
        return request.build_absolute_uri(relative_url)


class ParentDetailSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField(
        source='parent.user.email',
        read_only=True,
    )

    accepted_users = serializers.SerializerMethodField()
    rejected_users = serializers.SerializerMethodField()
    pending_users = serializers.SerializerMethodField()

    class Meta:
        model = ExchangeParent
        fields = [
            'parent',
            'status',
            'accepted_users',
            'rejected_users',
            'pending_users',
        ]

    def get_accepted_users(self, obj):
        accepted_users = ExchangeParent.objects.filter(
            parent=obj,
            status=ExchangeParent.ACCEPTED,
        )

        return ExchangeUserSerializer(
            [user_instance.user for user_instance in accepted_users],
            many=True,
            context=self.context,
        ).data

    def get_rejected_users(self, obj):
        rejected_users = ExchangeParent.objects.filter(
            parent=obj,
            status=ExchangeParent.REJECTED,
        )

        return ExchangeUserSerializer(
            [user_instance.user for user_instance in rejected_users],
            many=True,
            context=self.context,
        ).data

    def get_pending_users(self, obj):
        pending_users = ExchangeParent.objects.filter(
            parent=obj,
            status=ExchangeParent.PENDING
        )

        return ExchangeUserSerializer(
            [user_instance.user for user_instance in pending_users],
            many=True,
            context=self.context,
        ).data
