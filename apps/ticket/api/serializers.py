from rest_framework import serializers

from ticket.models import TicketDepartment

class TicketDepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDepartment
        fields = [
            'name',
            'icon',
            'is_active',
        ]
