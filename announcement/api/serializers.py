from rest_framework import serializers

from announcement.models import Announcements

class AnnouncementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = [
            'title',
            'author',
            'image',
            'summery',
            'text',
        ]
