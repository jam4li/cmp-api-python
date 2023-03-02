from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import models, BaseModel

from users.models import User
from withdraw.models import Withdraw
from voucher.models import Voucher
from payment.models import Payment
from cmp.models import CMPToken

# Create your models here.


class Transaction(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    withdraw = models.ForeignKey(
        Withdraw,
        on_delete=models.CASCADE,
        verbose_name=_('Withdraw'),
        blank=True,
        null=True,
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        verbose_name=_('Payment'),
        blank=True,
        null=True,
    )
    voucher = models.ForeignKey(
        Voucher,
        on_delete=models.CASCADE,
        verbose_name=_('Voucher'),
        blank=True,
        null=True,
    )
    cmp_token = models.ForeignKey(
        CMPToken,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        verbose_name=_('Amount'),
    )
    type = models.CharField(
        max_length=255,
        verbose_name=_('Type'),
    )
    status = models.BooleanField(
        default=False,
        verbose_name=_('Status'),
    )
    description = models.TextField(
        max_length=1000,
        verbose_name=_('Description'),
    )

    class Meta:
        db_table = 'transactions'
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return str(self.user)
