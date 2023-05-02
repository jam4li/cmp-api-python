from decimal import Decimal
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from apps.invest.models import Invest
from apps.users.models import User
from apps.package.models import Package


class SerializerTests(APITestCase):

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

        self.invest_list_url = reverse('invest_user:list')

    def test_invest_list_api_view(self):
        response = self.client.get(
            self.invest_list_url,
            HTTP_AUTHORIZATION=self.api_authentication_header,
        )

        # Assert the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'success': True,
            'code': 200,
            'data': [
                {
                    'id': self.invest.id,
                    'package': {
                        'id': self.package.id,
                        'name': None,
                        'price': '1000.00',
                        'image': None,
                    },
                    'invest': '1000.000',
                    'profit': '0.000',
                },
            ],
            'message': 'Data retrieved successfully',
        }

        self.assertEqual(response.data, expected_data)
