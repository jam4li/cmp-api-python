from rest_framework import serializers

from announcement.models import Announcement

class AnnouncementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'title',
            'author',
            'image',
            'summery',
            'text',
        ]
