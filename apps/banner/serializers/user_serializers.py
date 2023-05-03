from rest_framework import serializers

from apps.banner.models import Banner


class BannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            'title',
            'author',
            'image',
            'summary',
            'text',
            'publish_date',
        ]
