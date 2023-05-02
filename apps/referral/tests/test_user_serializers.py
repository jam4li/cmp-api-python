from django.test import TestCase

from apps.users.models import User
from apps.network.models import Network
from apps.referral.models import Referral
from apps.referral.serializers.user_serializers import (
    ReferralUserSerializer,
    ReferralDirectListSerializer,
    ReferralBinaryDetailSerializer,
)


class ReferralSerializerTests(TestCase):

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

    def test_referral_user_serializer(self):
        serializer = ReferralUserSerializer(instance=self.user1)
        expected_data = {
            'email': self.user1.email,
        }

        self.assertEqual(serializer.data, expected_data)

    def test_referral_direct_list_serializer(self):
        serializer = ReferralDirectListSerializer(instance=self.referral)
        expected_data = {
            'user': {
                'email': self.user1.email,
            },
        }

        self.assertEqual(serializer.data, expected_data)

    def test_referral_binary_detail_serializer(self):
        serializer = ReferralBinaryDetailSerializer(instance=self.network)
        expected_data = {
            'left_count': self.network.left_count,
            'right_count': self.network.right_count,
            'left_amount': format(self.network.left_amount, ".3f"),
            'right_amount': format(self.network.right_amount, ".3f"),
        }

        self.assertEqual(serializer.data, expected_data)
