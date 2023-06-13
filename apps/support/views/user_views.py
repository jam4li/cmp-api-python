from rest_framework import views, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from utils.response import ApiResponse

from apps.support.models import SupportDepartment, SupportTicket, SupportTicketReply
from apps.support.serializers.user_serializers import SupportDepartmentListSerializer, SupportTicketCreateSerializer, SupportTicketListSerializer, SupportTicketDetailSerializer


class SupportDepartmentListAPIView(views.APIView):
    def get(self, request, format=None):
        support_department = SupportDepartment.objects.all()
        serializer = SupportDepartmentListSerializer(
            support_department,
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


class SupportTicketCreateAPIView(views.APIView):
    def post(self, request):
        user = self.request.user

        has_support_ticket = SupportTicket.objects.filter(
            user=user,
            status="open",
        ).exists()

        if has_support_ticket:
            return Response({
                "success": False,
                "message": _("Failed to create support ticket."),
                "errors": serializer.errors,
            },
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class SupportTicketDetailAPIView(views.APIView):
    def get(self, request, pk, format=None):
        try:
            support_ticket = SupportTicket.objects.get(id=pk)
        except SupportTicket.DoesNotExist:
            pass

        support_ticket_reply_list = SupportTicketReply.objects.filter(
            ticket=support_ticket,
        )

        serializer = SupportTicketDetailSerializer(
            support_ticket_reply_list,
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

    def post(self, request, pk, format=None):
        try:
            support_ticket = SupportTicket.objects.get(id=pk)
        except SupportTicket.DoesNotExist:
            pass

        reply = self.request.data.get('reply')

        support_ticket.is_admin_replied = False
        support_ticket.save()

        SupportTicketReply.objects.create(
            ticket=support_ticket,
            content=reply,
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data={},
            message='Data created successfully'
        )

        return Response(success_response)
