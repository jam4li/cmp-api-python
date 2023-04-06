from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

from apps.users.models import User

# Create your models here.


class Wallet(BaseModel):
    DEPOSIT = "deposit"
    COMMISSION = "commission"
    PROFIT = "profit"
    CMP = "cmp"
    VOUCHER = "voucher"
    TYPE_CHOICES = (
        (DEPOSIT, _("Deposit")),
        (COMMISSION, _("Commission")),
        (PROFIT, _("Profit")),
        (CMP, _("Cmp")),
        (VOUCHER, _("Voucher")),
    )

    USER = "user"
    COMPANY = "company"
    ACCOUNTING = "accounting"
    ACCESS_TYPE_CHOICES = (
        (USER, _("User")),
        (COMPANY, _("Company")),
        (ACCOUNTING, _("Accounting")),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
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

    class Meta:
        db_table = 'wallets'
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')

    def __str__(self):
        return str(self.user)
