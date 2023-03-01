from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Users

# Create your models here.


class Voucher(models.Model):
    COMMISION = "commision"
    PROFIT = "profit"
    VOUCHER = "voucher"
    WALLET_TYPE_CHOICES = (
        (COMMISION, _("Commision")),
        (PROFIT, _("Profit")),
        (VOUCHER, _("Voucher")),
    )

    voucher = models.CharField(
        max_length=255,
        verbose_name=_('Voucher'),
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name=_('Amount'),
    )
    # TODO: creator_id
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    wallet_type = models.CharField(
        max_length=10,
        choices=WALLET_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name=_('Wallet type'),
    )
    cashed = models.BooleanField(
        default=False,
        verbose_name=_('Cashed'),
    )
    cashed_at = models.DateTimeField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    class Meta:
        db_table = 'vouchers'
        verbose_name = _('Voucher')
        verbose_name_plural = _('Vouchers')

    def __str__(self):
        return self.voucher
