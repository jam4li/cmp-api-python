from rest_framework import views
from rest_framework.response import Response

from apps.users.models import User
# from .serializers import AnnouncementListSerializer


class UserDashboardAPIView(views.APIView):
    def get(self, request, format=None):
        data = {
            "active_packages": "Pending",
            "balance": "Pending",
            "direct_invited": "Pending",
            "team": "Pending",
        }

        return Response(data)


class UserDetailAPIView(views.APIView):
    def get(self, request, format=None):
        data = {
            "name": "User",
        }

        return Response(data)
