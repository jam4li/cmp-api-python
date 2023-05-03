from decimal import Decimal
from django.test import TestCase

from apps.transaction.models import Transaction
from apps.users.models import User
from apps.withdraw.models import Withdraw
from apps.payment.models import Payment


class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@gmail.com',
            name='John Doe',
        )
        self.withdraw = Withdraw.objects.create(
            user=self.user,
            amount=Decimal('100.000'),
            fee=Decimal('10.000'),
            wallet_address='qwertyasdfghzxcvb',
            status=Withdraw.PENDING,
            wallet_type=Withdraw.PROFIT,
        )
        self.payment = Payment.objects.create(
            user=self.user,
            amount=Decimal('15.000'),
            status=Payment.SUCCESS,
            symbol=Payment.USDT,
        )

    def test_transaction_creation_with_withdraw(self):
        transaction = Transaction.objects.create(
            user=self.user,
            withdraw=self.withdraw,
            amount=Decimal('10.000'),
            type="Withdraw",
            status=True,
            description="Withdrawal transaction"
        )
        self.assertIsNotNone(
            transaction,
        )
        self.assertEqual(
            transaction.user,
            self.user,
        )
        self.assertEqual(
            transaction.withdraw,
            self.withdraw,
        )
        self.assertEqual(
            transaction.amount,
            Decimal('10.000'),
        )
        self.assertEqual(
            transaction.type,
            "Withdraw",
        )
        self.assertTrue(
            transaction.status,
        )
        self.assertEqual(
            transaction.description,
            "Withdrawal transaction",
        )

    def test_transaction_creation_with_payment(self):
        transaction = Transaction.objects.create(
            user=self.user,
            payment=self.payment,
            amount=Decimal('15.000'),
            type="Payment",
            status=True,
            description="Payment transaction"
        )
        self.assertIsNotNone(
            transaction,
        )
        self.assertEqual(
            transaction.user,
            self.user,
        )
        self.assertEqual(
            transaction.payment,
            self.payment,
        )
        self.assertEqual(
            transaction.amount,
            Decimal('15.000'),
        )
        self.assertEqual(
            transaction.type,
            "Payment",
        )
        self.assertTrue(
            transaction.status,
        )
        self.assertEqual(
            transaction.description,
            "Payment transaction",
        )
