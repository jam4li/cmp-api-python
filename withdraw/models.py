from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Users

# Create your models here.


class Withdraws(models.Model):
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    PENDING = "pending"
    STATUS_CHOICES = (
        (REJECTED, _("Rejected")),
        (ACCEPTED, _("Accepted")),
        (PENDING, _("Pending")),
    )

    COMMISION = "commision"
    PROFIT = "profit"
    WALLET_TYPE_CHOICES = (
        (COMMISION, _("Commision")),
        (PROFIT, _("Profit")),
    )

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_('Amount'),
    )
    fee = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_('Fee'),
    )
    wallet_address = models.CharField(
        max_length=255,
        verbose_name=_('Wallet address'),
    )
    transaction_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Transaction hash'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name=_('Status'),
    )
    wallet_type = models.CharField(
        max_length=10,
        choices=WALLET_TYPE_CHOICES,
        verbose_name=_('Wallet type'),
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
        db_table = 'withdraws'
        verbose_name = _('Withdraw')
        verbose_name_plural = _('Withdraws')

    def __str__(self):
        return self.wallet_address
