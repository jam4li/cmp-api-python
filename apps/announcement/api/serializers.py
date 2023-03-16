from rest_framework import serializers

from apps.announcement.models import Announcement


class AnnouncementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'title',
            'author',
            'image',
            'summery',
            'text',
            'publish_date',
        ]
