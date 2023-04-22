from rest_framework import views, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from apps.support.models import SupportDepartment, SupportTicket
from apps.support.serializers.user_serializers import SupportDepartmentListSerializer, SupportTicketCreateSerializer, SupportTicketListSerializer


class SupportDepartmentListAPIView(views.APIView):
    def get(self, request, format=None):
        support_department = SupportDepartment.objects.all()
        serializer = SupportDepartmentListSerializer(
            support_department,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)


class SupportTicketCreateAPIView(views.APIView):
    def post(self, request):
        user = self.request.user

        serializer = SupportTicketCreateSerializer(
            data=request.data,
            context={'request': request},
        )

        if serializer.is_valid(raise_exception=True):
            support_ticket = serializer.save(
                user=user,
            )

            return Response({
                "success": True,
                "message": _("Support ticket created successfully."),
                "ticket_id": support_ticket.id,
            },
                status=status.HTTP_201_CREATED,
            )

        return Response({
            "success": False,
            "message": _("Failed to create support ticket."),
            "errors": serializer.errors,
        },
            status=status.HTTP_400_BAD_REQUEST,
        )


class SupportTicketListAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        support_ticket = SupportTicket.objects.filter(user=user)

        serializer = SupportTicketListSerializer(
            support_ticket,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)
