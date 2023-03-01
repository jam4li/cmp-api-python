from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Users

# Create your models here.


class Wallet(models.Model):
    DEPOSIT = "rejected"
    COMMISION = "accepted"
    PROFIT = "pending"
    CMP = "cmp"
    VOUCHER = "voucher"
    TYPE_CHOICES = (
        (DEPOSIT, _("Deposit")),
        (COMMISION, _("Commision")),
        (PROFIT, _("Profit")),
        (CMP, _("Cmp")),
        (VOUCHER, _("Voucher")),
    )

    USER = "user"
    COMPANY = "company"
    ACCOUNTING = "accounting"
    ACCESS_TYPE_CHOICES = (
        (COMMISION, _("Commision")),
        (PROFIT, _("Profit")),
    )

    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name=_('type'),
    )
    access_type = models.CharField(
        max_length=10,
        choices=ACCESS_TYPE_CHOICES,
        verbose_name=_('Access type'),
    )
    balance = models.DecimalField(
        default=0.000,
        max_digits=30,
        decimal_places=3,
        verbose_name=_('Balance'),
    )
    blocked_amount = models.DecimalField(
        default=0.000,
        max_digits=30,
        decimal_places=3,
        verbose_name=_('Blocked amount'),
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
        db_table = 'wallets'
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')

    def __str__(self):
        return self.title


class UserWallet(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name=_('User'))
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name=_('Wallet'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    class Meta:
        db_table = 'user_wallet'
        verbose_name = _('User wallet')
        verbose_name_plural = _('User wallets')

    def __str__(self):
        return self.user
