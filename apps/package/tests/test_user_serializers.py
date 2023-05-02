from decimal import Decimal
from django.test import TestCase

from apps.package.models import Package
from apps.package.serializers.user_serializers import PackageListSerializer, PackageBuySerializer


class SerializerTests(TestCase):

    def setUp(self):
        self.package = Package.objects.create(
            name='Test Package',
            price=Decimal('1000.00'),
            status=True,
            fee=Decimal('10.00'),
            daily_profit=Decimal('5'),
            daily_profit_percent='0.5%',
            profit_limit=Decimal('1000')
        )

    def test_package_list_serializer(self):
        serializer = PackageListSerializer(self.package)

        expected_data = {
            'id': self.package.id,
            'name': 'Test Package',
            'price': '1000.00',
            'image': None,
            'summary': None,
            'fee': '10.00',
            'daily_profit': '5',
            'daily_profit_percent': '0.5%',
            'profit_limit': '1000',
        }

        self.assertEqual(serializer.data, expected_data)

    def test_package_buy_serializer(self):
        data = {
            'id': 1,
            'symbol': 'BTC',
            'voucher_amount': 0,
        }

        serializer = PackageBuySerializer(data=data)
        self.assertTrue(serializer.is_valid())

        expected_data = {
            'id': 1,
            'symbol': 'BTC',
            'voucher_amount': 0,
        }

        self.assertEqual(serializer.validated_data, expected_data)
