from django.urls import reverse
from django.http import HttpRequest
from rest_framework import serializers
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.users.models import User

from apps.exchange.models import ExchangeParent
from apps.exchange.serializers.user_serializers import (
    CMEXBITUserSerializer,
    CMEXBITExchangeParentSeiralizer,
    ExchangeUserSerializer,
    ParentDetailSerializer,
)


class SerializerTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(
            email="user1@gmail.com",
            name="User 1"
        )
        cls.user2 = User.objects.create(
            email="user2@gmail.com",
            name="User 2"
        )
        cls.exchange_parent1 = ExchangeParent.objects.create(
            user=cls.user1,
            status=ExchangeParent.PENDING
        )
        cls.exchange_parent2 = ExchangeParent.objects.create(
            user=cls.user2,
            parent=cls.exchange_parent1,
            status=ExchangeParent.PENDING
        )
        cls.token = Token.objects.create(
            user=cls.user2,
        )

        cls.api_authentication_header = f'Token {cls.token.key}'

    def test_cmexbit_user_serializer(self):
        serializer = CMEXBITUserSerializer(self.user1)
        expected_data = {
            'email': self.user1.email,
            'name': self.user1.name,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_cmexbit_exchange_parent_serializer(self):
        serializer = CMEXBITExchangeParentSeiralizer(self.exchange_parent2)
        expected_data = {
            'user': CMEXBITUserSerializer(self.user2).data,
            'parent': CMEXBITUserSerializer(self.user1).data,
            'status': self.exchange_parent2.status,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_exchange_user_serializer(self):
        # Create a fake HttpRequest object and update it with the necessary data
        request = HttpRequest()
        request.META['SERVER_NAME'] = 'testserver'
        request.META['SERVER_PORT'] = '80'
        request.META['HTTP_AUTHORIZATION'] = self.api_authentication_header

        serializer = ExchangeUserSerializer(self.user1)
        expected_data = {
            'email': self.user1.email,
            'accept_url': request.build_absolute_uri(
                reverse(
                    "exchange_user:accept-user",
                    kwargs={"user_id": self.user1.id},
                ),
            ),
            'reject_url': request.build_absolute_uri(
                reverse(
                    "exchange_user:reject-user",
                    kwargs={"user_id": self.user1.id},
                ),
            ),
        }
        self.assertEqual(serializer.data, expected_data)

    def test_parent_detail_serializer(self):
        # Create a fake HttpRequest object and update it with the necessary data
        request = HttpRequest()
        request.META['SERVER_NAME'] = 'testserver'
        request.META['SERVER_PORT'] = '80'
        request.META['HTTP_AUTHORIZATION'] = self.api_authentication_header

        serializer = ParentDetailSerializer(
            self.exchange_parent1,
            context={"request": request},
        )

        expected_data = {
            'parent': None,
            'status': self.exchange_parent1.status,
            'accepted_users': [],
            'rejected_users': [],
            'pending_users': [
                ExchangeUserSerializer(
                    self.user2,
                    context={"request": request},
                ).data,
            ],
        }
        self.assertEqual(
            serializer.data,
            expected_data,
        )
