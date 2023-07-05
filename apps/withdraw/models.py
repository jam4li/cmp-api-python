from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

from apps.users.models import User
from apps.wallet.models import Wallet

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
        verbose_name = _('Withdraw')
        verbose_name_plural = _('Withdraws')

    def __str__(self):
        return self.wallet_address

    def save(self, *args, **kwargs):
        # Check if the status has changed from pending to rejected
        if self.pk and self.status == self.REJECTED and self._state.adding is False:
            original_status = Withdraw.objects.get(pk=self.pk).status

            if original_status == self.PENDING:

                try:
                    wallet = Wallet.objects.get(
                        user=self.user,
                        type=self.wallet_type,
                    )

                except Wallet.DoesNotExist:
                    return False

                wallet.balance += self.amount + self.fee
                wallet.save()

        super().save(*args, **kwargs)
