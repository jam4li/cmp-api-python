from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

from apps.users.models import User
from apps.package.models import Package

# Create your models here.


class Invest(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        verbose_name=_('Package'),
    )
    invest = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        verbose_name=_('Invest'),
    )
    profit = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Profit'),
    )
    payout_binary_status = models.BooleanField(
        default=False,
        verbose_name=_('Payout binary status'),
    )
    payout_direct_status = models.BooleanField(
        default=False,
        verbose_name=_('Payout direct status'),
    )
    finished = models.BooleanField(
        default=False,
        verbose_name=_('Finished'),
    )
    calculated_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Invest')
        verbose_name_plural = _('Invests')

    def __str__(self):
        return str(self.user)
