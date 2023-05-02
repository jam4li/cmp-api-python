from decimal import Decimal
from django.test import TestCase

from apps.package.models import Package


class ModelTests(TestCase):

    def setUp(self):
        self.package = Package.objects.create(
            name='Test Package',
            price=Decimal('1000.00'),
            status=True,
            fee=Decimal('10.00'),
            daily_profit=Decimal('5.00'),
            daily_profit_percent='0.5%',
            profit_limit=Decimal('1000.00')
        )

    def test_package_creation(self):
        self.assertIsInstance(self.package, Package)

    def test_package_fields(self):
        self.assertEqual(
            self.package.name,
            'Test Package',
        )
        self.assertEqual(
            self.package.price,
            Decimal('1000.00'),
        )
        self.assertEqual(
            self.package.sort,
            1,
        )
        self.assertEqual(
            self.package.status,
            True,
        )
        self.assertEqual(
            self.package.fee,
            Decimal('10.00'),
        )
        self.assertEqual(
            self.package.daily_profit,
            Decimal('5.00'),
        )
        self.assertEqual(
            self.package.daily_profit_percent,
            '0.5%',
        )
        self.assertEqual(
            self.package.profit_limit,
            Decimal('1000.00'),
        )
