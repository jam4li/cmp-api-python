from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.announcement.models import Announcement
from apps.announcement.serializers.user_serializers import AnnouncementListSerializer


class AnnouncementListAPIView(views.APIView):
    def get(self, request, format=None):
        announcements = Announcement.objects.filter(
            status="publish",
        ).order_by(
            'publish_date',
        )

        serializer = AnnouncementListSerializer(
            announcements,
            many=True,
            context={"request": request},
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)
