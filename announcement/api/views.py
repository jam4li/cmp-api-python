from rest_framework import views
from rest_framework.response import Response

from announcement.models import Announcement
from .serializers import AnnouncementListSerializer


class AnnouncementListAPIView(views.APIView):
    def get(self, request, format=None):
        announcements = Announcement.objects.filter(
            status="publish",
        ).order_by(
            'publish_date',
        )

        serializer = AnnouncementListSerializer(announcements, many=True)

        return Response(serializer.data)
