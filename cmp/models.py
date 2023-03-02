from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User

# Create your models here.


class CMPToken(models.Model):
    PROFIT = "profit"
    COMMISSION = "commission"
    WALLET_TYPE_CHOICES = (
        (PROFIT, _("Profit")),
        (COMMISSION, _("Commission")),
    )

    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed"
    STATUS_CHOICES = (
        (SUCCESS, _("Success")),
        (PENDING, _("Pending")),
        (FAILED, _("Failed")),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    transaction_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Transaction hash'),
    )
    cmp_token_amount = models.DecimalField(
        max_digits=30,
        decimal_places=4,
        verbose_name=_('Cmp token amount')
    )
    input_amount = models.DecimalField(
        max_digits=30,
        decimal_places=4,
        verbose_name=_('Input amount'),
    )
    fee_amount = models.DecimalField(
        max_digits=30,
        decimal_places=4,
        verbose_name=_('Fee amount'),
    )
    fee_percent = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Fee percent'),
    )
    cmp_per_usd_unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Cmp per usd unit price'),
    )
    wallet_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Wallet address'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    class Meta:
        db_table = 'cmp_tokens'
        verbose_name = _('CMP Token')
        verbose_name_plural = _('CMP Tokens')

    def __str__(self):
        return self.transaction_hash
