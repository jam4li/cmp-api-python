from django.test import TestCase

from apps.users.models import User
from apps.network.models import Network
from apps.referral.models import Referral


class ReferralModelTests(TestCase):

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

    def test_create_referral(self):
        self.assertEqual(
            self.referral.user,
            self.user1,
        )
        self.assertEqual(
            self.referral.network,
            self.network,
        )
        self.assertEqual(
            self.referral.referrer,
            self.user2,
        )
        self.assertEqual(
            self.referral.recruited,
            Referral.LEFT,
        )
        self.assertEqual(
            self.referral.binary_place,
            '0,1',
        )

    def test_recruited_choices(self):
        self.assertIn(
            Referral.LEFT,
            dict(Referral.RECRUITED_CHOICES),
        )
        self.assertIn(
            Referral.RIGHT,
            dict(Referral.RECRUITED_CHOICES),
        )
        self.assertEqual(
            Referral.RECRUITED_CHOICES[0][1].__str__(),
            "Right",
        )
        self.assertEqual(
            Referral.RECRUITED_CHOICES[1][1].__str__(),
            "Left",
        )
