from decimal import Decimal
from django.test import TestCase

from apps.users.models import User
from apps.payment.models import Payment


class PaymentModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@gmail.com',
            name='John Doe',
        )
        self.payment = Payment.objects.create(
            payment_hash='1234567890abcdef',
            payment_code='PAY-123456',
            amount=Decimal('100.000'),
            user=self.user,
            status=Payment.PENDING,
            symbol=Payment.USDT,
            charge=10,
        )

    def test_payment_creation(self):
        self.assertEqual(
            self.payment.payment_hash,
            '1234567890abcdef',
        )
        self.assertEqual(
            self.payment.payment_code,
            'PAY-123456',
        )
        self.assertEqual(
            self.payment.amount,
            Decimal('100.000'),
        )
        self.assertEqual(
            self.payment.user,
            self.user,
        )
        self.assertEqual(
            self.payment.status,
            Payment.PENDING,
        )
        self.assertEqual(
            self.payment.symbol,
            Payment.USDT,
        )
        self.assertEqual(
            self.payment.charge,
            10,
        )

    def test_status_choices(self):
        self.assertEqual(
            Payment.SUCCESS,
            'success',
        )
        self.assertEqual(
            Payment.PENDING,
            'pending',
        )
        self.assertEqual(
            Payment.FAILED,
            'failed',
        )

    def test_symbol_choices(self):
        self.assertEqual(
            Payment.USDT,
            'USDT',
        )
        self.assertEqual(
            Payment.CMP,
            'CMP',
        )

    def test_str_representation(self):
        self.assertEqual(str(self.payment), '1234567890abcdef')
