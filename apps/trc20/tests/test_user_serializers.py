from django.test import TestCase
from rest_framework import serializers

from apps.trc20.models import Trc20
from apps.trc20.serializers.user_serializers import Trc20CreateGatewaySerializer


class Trc20CreateGatewaySerializerTest(TestCase):
    def setUp(self):
        self.trc20_data = {
            'amount': 100.0,
            'payment_code': 'test_payment_code',
            'user_id': 'test_user_id',
            'symbol': 'test_symbol',
            'callback_url': 'https://test.com/callback',
        }

        self.trc20_obj = Trc20.objects.create(**self.trc20_data)

    def test_serializer_data(self):
        serializer = Trc20CreateGatewaySerializer(self.trc20_obj)
        expected_data = {
            'amount': 100.0,
            'payment_code': 'test_payment_code',
            'user_id': 'test_user_id',
            'symbol': 'test_symbol',
            'callback_url': 'https://test.com/callback',
        }
        self.assertEqual(
            serializer.data,
            expected_data,
        )

    def test_serializer_validation(self):
        serializer = Trc20CreateGatewaySerializer(
            data=self.trc20_data,
        )

        self.assertTrue(serializer.is_valid())

        # TODO: Fix the below test
        # invalid_data = self.trc20_data.copy()
        # invalid_data['amount'] = -1
        # serializer = Trc20CreateGatewaySerializer(data=invalid_data)

        # self.assertFalse(serializer.is_valid())
        # self.assertIn(
        #     'amount',
        #     serializer.errors,
        # )
