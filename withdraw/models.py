from django.utils.translation import gettext_lazy as _

from base.models import models, BaseModel

from users.models import User

# Create your models here.


class Withdraw(BaseModel):
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
        User,
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

    class Meta:
        db_table = 'withdraws'
        verbose_name = _('Withdraw')
        verbose_name_plural = _('Withdraws')

    def __str__(self):
        return self.wallet_address
