from rest_framework.test import APITestCase
from django.urls import reverse
from django.http import HttpRequest
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.users.models import User
from apps.exchange.models import ExchangeParent
from apps.exchange.serializers.user_serializers import (
    CMEXBITUserSerializer,
    ParentDetailSerializer,
    CMEXBITExchangeParentSeiralizer,
)


class TestExchangeParentViews(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email='test1@gmail.com',
            name='John Doe 1',
        )
        self.user2 = User.objects.create(
            email='test2@gmail.com',
            name='John Doe 2',
        )

        self.exchange_parent1 = ExchangeParent.objects.create(
            user=self.user1,
        )
        self.exchange_parent2 = ExchangeParent.objects.create(
            user=self.user2,
            parent=self.exchange_parent1,
        )

        self.cmexbit_url = reverse('exchange_user:bitmex')
        self.parent_create_url = reverse('exchange_user:parent-create')
        self.parent_detail_url = reverse('exchange_user:parent-detail')
        self.accept_user_url = reverse(
            'exchange_user:accept-user',
            kwargs={'user_id': self.user1.id},
        )
        self.reject_user_url = reverse(
            'exchange_user:reject-user',
            kwargs={'user_id': self.user1.id},
        )

        self.token = Token.objects.create(
            user=self.user2,
        )

        self.api_authentication_header = f'Token {self.token.key}'

    def test_cmexbit_api_view_post(self):
        response = self.client.post(
            self.cmexbit_url,
            data={'email': self.user2.email},
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        serializer = CMEXBITExchangeParentSeiralizer(
            self.exchange_parent2,
        )
        self.assertEqual(
            response.data['data'],
            serializer.data,
        )

    def test_parent_create_api_view_post(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )
        response = self.client.post(
            self.parent_create_url,
            data={'parent_email': self.user1.email},
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['exchange_parent'],
            str(self.exchange_parent1),
        )

    def test_parent_detail_api_view_get(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )
        response = self.client.get(
            self.parent_detail_url,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        # Create a fake HttpRequest object and update it with the necessary data
        request = HttpRequest()
        request.META['SERVER_NAME'] = 'testserver'
        request.META['SERVER_PORT'] = '80'
        request.META['HTTP_AUTHORIZATION'] = self.api_authentication_header

        serializer = ParentDetailSerializer(
            self.exchange_parent2,
            context={'request': request},
        )
        self.assertEqual(
            response.data['data'],
            serializer.data,
        )

    def test_accept_user_view_get(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )
        response = self.client.get(
            self.accept_user_url,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.exchange_parent1.refresh_from_db()
        self.assertEqual(
            self.exchange_parent1.status,
            ExchangeParent.ACCEPTED,
        )

    def test_reject_user_view_get(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )
        response = self.client.get(
            self.reject_user_url,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.exchange_parent1.refresh_from_db()
        self.assertEqual(
            self.exchange_parent1.status,
            ExchangeParent.REJECTED,
        )
