from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.package.models import Package
from apps.users.models import User


class PackageAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@gmail.com',
            name='John Doe',
        )
        self.token = Token.objects.create(
            user=self.user,
        )
        self.api_authentication_header = f'Token {self.token.key}'

        self.package = Package.objects.create(
            name='Test Package',
            price=Decimal('1000.00'),
            fee=Decimal('10.00'),
            daily_profit=Decimal('5.00'),
            daily_profit_percent='0.5%',
            profit_limit=Decimal('1500.00'),
            status=True,
        )

        self.package_list_url = reverse('package_user:list')
        self.package_buy_url = reverse('package_user:buy')

    def test_package_list_api_view(self):
        response = self.client.get(
            self.package_list_url,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_buy_api_view(self):
        data = {
            'id': self.package.id,
            'symbol': 'USDT',
            'voucher_amount': 0,
        }
        response = self.client.post(
            self.package_buy_url,
            data,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.package.id)
        self.assertEqual(response.data['symbol'], 'USDT')
