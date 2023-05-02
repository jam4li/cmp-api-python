from django.test import TestCase
from apps.users.models import User

from apps.exchange.models import ExchangeParent


class TestExchangeParentModel(TestCase):
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

    def test_exchange_parent_creation(self):
        self.assertIsNotNone(self.exchange_parent1)
        self.assertIsNotNone(self.exchange_parent2)

    def test_exchange_parent_status_default(self):
        self.assertEqual(self.exchange_parent1.status, ExchangeParent.PENDING)

    def test_exchange_parent_str_representation(self):
        self.assertEqual(str(self.exchange_parent1), 'test1@gmail.com')

    def test_exchange_parent_user_relation(self):
        self.assertEqual(self.exchange_parent1.user, self.user1)

    def test_exchange_parent_parent_relation(self):
        self.assertIsNone(self.exchange_parent1.parent)
        self.assertEqual(self.exchange_parent2.parent, self.exchange_parent1)
