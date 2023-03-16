from rest_framework import views
from rest_framework.response import Response

from ticket.models import TicketDepartment
from .serializers import TicketDepartmentListSerializer


class TicketDepartmentListAPIView(views.APIView):
    def get(self, request, format=None):
        ticket_department = TicketDepartment.objects.all()
        serializer = TicketDepartmentListSerializer(
            ticket_department,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)
