from django.test import TestCase

from apps.trc20.models import Trc20


class Trc20ModelTest(TestCase):
    def setUp(self):
        self.trc20 = Trc20.objects.create(
            invoice_id='test_invoice_01',
            amount=100.0,
            payment_code='test_payment_code',
            user_id='test_user_id',
            symbol='test_symbol',
            callback_url='https://test.com/callback',
            status=Trc20.PENDING,
        )

    def test_trc20_creation(self):
        self.assertIsInstance(
            self.trc20,
            Trc20,
        )
        self.assertEqual(
            self.trc20.invoice_id,
            'test_invoice_01',
        )
        self.assertEqual(
            self.trc20.amount,
            100.0,
        )
        self.assertEqual(
            self.trc20.payment_code,
            'test_payment_code',
        )
        self.assertEqual(
            self.trc20.user_id,
            'test_user_id',
        )
        self.assertEqual(
            self.trc20.symbol,
            'test_symbol',
        )
        self.assertEqual(
            self.trc20.callback_url,
            'https://test.com/callback',
        )
        self.assertEqual(
            self.trc20.status,
            Trc20.PENDING,
        )
