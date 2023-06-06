from rest_framework import serializers

from apps.support.models import SupportTicket, SupportDepartment, SupportTicketReply


class SupportDepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportDepartment
        fields = [
            'id',
            'name',
            'icon',
            'is_active',
        ]


class SupportTicketCreateSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=SupportDepartment.objects.all(),
    )

    class Meta:
        model = SupportTicket
        fields = (
            'department',
            'title',
            'content',
        )


class SupportTicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = [
            'id',
            'title',
            'content',
            'created_at',
        ]


class SupportTicketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicketReply
        fields = [
            'content',
        ]
