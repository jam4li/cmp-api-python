from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

from apps.users.models import User
from apps.purchase.models import Purchase

# Create your models here.


class Trc20(BaseModel):
    PENDING = 0
    PAID = 1
    UNDERPAID = 2
    OVERPAID = 3
    EXPIRED = 4
    CANCELLED = 5
    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (PAID, _("Paid")),
        (UNDERPAID, _("Under paid")),
        (OVERPAID, _("Over paid")),
        (EXPIRED, _("Expired")),
        (CANCELLED, _("Cancelled")),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        verbose_name=_('Purchase'),
    )
    message = invoice_id = models.CharField(
        max_length=50,
        verbose_name=_('Message'),
    )
    invoice_id = models.CharField(
        max_length=20,
        verbose_name=_('Invoice id'),
    )
    merchant_id = models.CharField(
        max_length=20,
        verbose_name=_('Merchant id'),
    )
    total_amount = models.FloatField(
        verbose_name=_('Total amount'),
    )
    paid_amount = models.FloatField(
        default=0.0,
        verbose_name=_('Paid amount'),
    )
    address = models.CharField(
        max_length=40,
        verbose_name=_('Address'),
    )
    url = models.CharField(
        max_length=40,
        verbose_name=_('Url'),
    )
    symbol = models.CharField(
        max_length=20,
        verbose_name=_('Symbol'),
    )
    status = models.SmallIntegerField(
        default=0,
        choices=STATUS_CHOICES,
        verbose_name=_('Status'),
    )
    payment_txid = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name=_('Payment txid'),
    )
    payment_confirmation = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Payment confirmation'),
    )
    expired_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Expired at'),
    )

    class Meta:
        verbose_name = _('Trc20')
        verbose_name_plural = _('Trc20')

    def __str__(self):
        return self.invoice_id
