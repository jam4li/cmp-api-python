from django.utils.translation import gettext_lazy as _

from base.models import models, BaseModel

from users.models import User

# Create your models here.


class Voucher(BaseModel):
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
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Creator'),
        related_name='voucher_creator',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('User'),
        related_name='voucer_user',
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
    cashed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'vouchers'
        verbose_name = _('Voucher')
        verbose_name_plural = _('Vouchers')

    def __str__(self):
        return self.voucher
