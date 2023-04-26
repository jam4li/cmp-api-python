from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from utils.response import ApiResponse

from apps.users.models import User
from apps.exchange.models import ExchangeParent

from apps.exchange.serializers.user_serializers import ParentDetailSerializer, CMEXBITExchangeParentSeiralizer


class CMEXBITApiView(views.APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        email = self.request.data.get('email')
        user = User.objects.get(email=email)
        exchange_parent = ExchangeParent.objects.get(user=user)

        serializer = CMEXBITExchangeParentSeiralizer(exchange_parent)

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class ParentCreateAPIView(views.APIView):
    def post(self, request):
        user = self.request.user

        parent_email = self.request.data.get('parent_email')

        # TODO: Add User.DoesnotExist handler
        parent_user = User.objects.get(email=parent_email)

        exchange_parent = ExchangeParent.objects.get(
            user=parent_user,
        )

        exchange_children, _ = ExchangeParent.objects.get_or_create(
            user=user,
        )

        exchange_children.parent = exchange_parent
        exchange_children.save()

        data = {
            'exchange_parent': str(exchange_children.parent),
        }

        return Response(data)


class ParentDetailAPIView(views.APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            exchange_parent = ExchangeParent.objects.get(user=user)

            serializer = ParentDetailSerializer(
                exchange_parent,
                context={"request": request},
            )

            success_response = ApiResponse(
                success=True,
                code=200,
                data=serializer.data,
                message='Data retrieved successfully'
            )

            return Response(success_response)

        except ExchangeParent.DoesNotExist:
            success_response = ApiResponse(
                success=True,
                code=200,
                data={},
                message='Data retrieved successfully'
            )

            return Response(success_response)


class AcceptUserView(views.APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(
            id=user_id,
        )

        exchange_parent = ExchangeParent.objects.get(
            user=user,
        )
        exchange_parent.status = 'accepted'
        exchange_parent.save()

        return Response({'status': 'Accepted'})


class RejectUserView(views.APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = User.objects.get(
            id=user_id,
        )

        exchange_parent = ExchangeParent.objects.get(
            user=user,
        )
        exchange_parent.status = 'rejected'
        exchange_parent.save()

        return Response({'status': 'Rejected'})
