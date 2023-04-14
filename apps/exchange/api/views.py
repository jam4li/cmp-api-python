from rest_framework import views
from rest_framework.response import Response

from apps.users.models import User
from apps.exchange.models import ExchangeParent


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
