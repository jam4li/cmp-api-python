from rest_framework import views
from rest_framework.response import Response

from support.models import SupportDepartment
from .serializers import SupportDepartmentListSerializer


class SupportDepartmentListAPIView(views.APIView):
    def get(self, request, format=None):
        support_department = SupportDepartment.objects.all()
        serializer = SupportDepartmentListSerializer(
            support_department,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)
