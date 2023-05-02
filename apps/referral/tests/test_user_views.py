from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.users.models import User
from apps.network.models import Network
from apps.referral.models import Referral
from apps.referral.serializers.user_serializers import ReferralDirectListSerializer, ReferralBinaryDetailSerializer


class ReferralAPIViewTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            email='test1@gmail.com',
            name='John Doe',
        )

        self.user2 = User.objects.create(
            email='test2@gmail.com',
            name='Jane Doe',
        )

        self.network = Network.objects.create(
            user=self.user1,
        )

        self.referral = Referral.objects.create(
            user=self.user1,
            network=self.network,
            referrer=self.user2,
            recruited=Referral.LEFT,
            binary_place='0,1',
        )

        self.token = Token.objects.create(
            user=self.user1,
        )
        self.api_authentication_header = f'Token {self.token.key}'

        self.referral_direct_list_url = reverse(
            'referral_user:direct-list',
        )
        self.referral_binary_detail_url = reverse(
            'referral_user:binary-detail',
        )

    def test_referral_direct_list_api_view(self):
        response = self.client.get(
            self.referral_direct_list_url,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )

        referrals = Referral.objects.filter(referrer=self.user1)
        serializer = ReferralDirectListSerializer(referrals, many=True)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['success'],
            True,
        )
        self.assertEqual(
            response.data['code'],
            200,
        )
        self.assertEqual(
            response.data['data'],
            serializer.data,
        )
        self.assertEqual(
            response.data['message'],
            'Data retrieved successfully',
        )

    def test_referral_binary_detail_api_view(self):
        response = self.client.get(
            self.referral_binary_detail_url,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )

        network = Network.objects.get(user=self.user1)
        serializer = ReferralBinaryDetailSerializer(network)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['success'],
            True,
        )
        self.assertEqual(
            response.data['code'],
            200,
        )
        self.assertEqual(
            response.data['data'],
            serializer.data,
        )
        self.assertEqual(
            response.data['message'],
            'Data retrieved successfully',
        )
