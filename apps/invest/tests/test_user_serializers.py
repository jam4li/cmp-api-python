from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from rest_framework import serializers

from apps.invest.models import Invest
from apps.users.models import User
from apps.package.models import Package

from apps.invest.serializers.user_serializers import PackageInvestListSerializer, InvestListSerializer


class SerializerTests(TestCase):

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

    def test_package_invest_list_serializer(self):
        serializer = PackageInvestListSerializer(self.package)

        expected_data = {
            'id': self.package.id,
            'name': None,
            'price': '1000.00',
            'image': None,
        }

        self.assertEqual(serializer.data, expected_data)

    def test_invest_list_serializer(self):
        serializer = InvestListSerializer(self.invest)

        expected_data = {
            'id': self.invest.id,
            'package': {
                'id': self.package.id,
                'name': None,
                'price': '1000.00',
                'image': None,
            },
            'invest': '1000.000',
            'profit': '0.000',
        }

        self.assertEqual(serializer.data, expected_data)
