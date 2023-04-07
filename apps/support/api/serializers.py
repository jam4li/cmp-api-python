from rest_framework import serializers

from support.models import SupportDepartment


class SupportDepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportDepartment
        fields = [
            'name',
            'icon',
            'is_active',
        ]
