from decimal import Decimal
from django.test import TestCase
from django.utils import timezone

from apps.invest.models import Invest
from apps.users.models import User
from apps.package.models import Package


class InvestModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@gmail.com',
            name='John Doe',
        )
        self.package = Package.objects.create(
            price=Decimal('1000.000'),
            fee=Decimal('10.000'),
        )
        self.invest = Invest.objects.create(
            user=self.user,
            package=self.package,
            invest=Decimal('1000.000'),
            total_invest=Decimal('2000.000'),
            calculated_at=timezone.now(),
        )

    def test_create_invest_instance(self):
        self.assertEqual(
            self.invest.user,
            self.user,
        )
        self.assertEqual(
            self.invest.package,
            self.package,
        )
        self.assertEqual(
            self.invest.invest,
            Decimal('1000.000'),
        )
        self.assertEqual(
            self.invest.total_invest,
            Decimal('2000.000'),
        )
        self.assertEqual(
            self.invest.profit,
            Decimal('0.000'),
        )
        self.assertEqual(
            self.invest.payout_binary_status,
            False,
        )
        self.assertEqual(
            self.invest.payout_direct_status,
            False,
        )
        self.assertEqual(
            self.invest.finished,
            False,
        )

    def test_update_invest_fields(self):
        self.invest.profit = Decimal('500.000')
        self.invest.finished = True
        self.invest.save()

        updated_invest = Invest.objects.get(pk=self.invest.pk)
        self.assertEqual(updated_invest.profit, Decimal('500.000'))
        self.assertEqual(updated_invest.finished, True)

    def test_invest_user_relation(self):
        user_invests = Invest.objects.filter(user=self.user)
        self.assertEqual(user_invests.last(), self.invest)
