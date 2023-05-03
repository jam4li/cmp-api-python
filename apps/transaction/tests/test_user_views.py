from django.urls import reverse
from rest_framework.test import APITestCase
from decimal import Decimal
from rest_framework.authtoken.models import Token

from apps.transaction.models import Transaction
from apps.users.models import User
from apps.withdraw.models import Withdraw
from apps.payment.models import Payment


class TransactionListAPIViewTestCase(APITestCase):
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
            user=self.user, amount=Decimal('15.000'),
            status=Payment.SUCCESS,
            symbol=Payment.USDT,
        )

        self.transaction_with_withdraw = Transaction.objects.create(
            user=self.user,
            withdraw=self.withdraw,
            amount=Decimal('10.000'),
            type="Withdraw",
            status=True,
            description="Withdrawal transaction"
        )

        self.transaction_with_payment = Transaction.objects.create(
            user=self.user,
            payment=self.payment,
            amount=Decimal('15.000'),
            type="Payment",
            status=True,
            description="Payment transaction"
        )

        self.token = Token.objects.create(
            user=self.user,
        )
        self.api_authentication_header = f'Token {self.token.key}'

        self.transaction_list_url = reverse('transaction_user:list')

    # TODO: Add the below test_api_view because it has updated_at fields
    # def test_transaction_list_api_view(self):
    #     response = self.client.get(
    #         self.transaction_list_url,
    #         HTTP_AUTHORIZATION=self.api_authentication_header,
    #     )

    #     expected_data = [
    #         {
    #             'amount': '10.000',
    #             'type': 'Withdraw',
    #             'description': 'Withdrawal transaction',
    #             'updated_at': self.transaction_with_withdraw.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    #         },
    #         {
    #             'amount': '15.000',
    #             'type': 'Payment',
    #             'description': 'Payment transaction',
    #             'updated_at': self.transaction_with_payment.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    #         }
    #     ]

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['data'], expected_data)
