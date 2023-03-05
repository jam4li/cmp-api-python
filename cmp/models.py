from django.utils.translation import gettext_lazy as _

from base.models import models, BaseModel

from users.models import User
from package.models import Package

# Create your models here.


class CMPToken(BaseModel):
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
    wallet_type = models.CharField(
        max_length=15,
        choices=WALLET_TYPE_CHOICES,
        verbose_name=_('Wallet type'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name=_('Status'),
    )

    class Meta:
        db_table = 'cmp_tokens'
        verbose_name = _('CMP Token')
        verbose_name_plural = _('CMP Tokens')

    def __str__(self):
        return self.transaction_hash


class CMPClaimHistory(BaseModel):
    wallet = models.CharField(
        max_length=255,
        verbose_name=_('Wallet'),
    )
    transaction_hash = models.CharField(
        max_length=255,
        verbose_name=_('Transaction hash'),
    )
    amount = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )
    profit = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )
    total_claim = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )
    locked_at = models.DateTimeField(
        verbose_name=_('Locked at'),
    )
    unlocked_at = models.DateTimeField(
        verbose_name=_('Unlocked at'),
    )

    class Meta:
        db_table = 'cmp_claim_histories'
        verbose_name = _('CMP Claim History')
        verbose_name_plural = _('CMP Claim Histories')

    def __str__(self):
        return self.wallet


class CMPTokenTransaction(BaseModel):
    payment = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        verbose_name=_('Payment'),
    )
    cmp_token = models.ForeignKey(
        CMPToken,
        on_delete=models.CASCADE,
        verbose_name=_('CMP token'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    amount = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )
    type = models.CharField(
        max_length=255,
        verbose_name=_('Type'),
    )
    status = models.BooleanField(
        default=True,
        verbose_name=_('Status'),
    )
    description = models.TextField(
        max_length=1000,
        verbose_name=_('Description'),
    )

    class Meta:
        db_table = 'cmp_token_transactions'
        verbose_name = _('CMP Token Transaction')
        verbose_name_plural = _('CMP Token Transactions')

    def __str__(self):
        return str(self.user)
