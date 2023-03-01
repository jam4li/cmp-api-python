from rest_framework import serializers

from banner.models import Banners

class BannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = [
            'big_title',
            'small_title',
            'image',
        ]
