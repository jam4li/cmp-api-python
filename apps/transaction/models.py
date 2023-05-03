from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

from apps.users.models import User
from apps.withdraw.models import Withdraw
from apps.payment.models import Payment

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
