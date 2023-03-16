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
    total_invest = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        verbose_name=_('Total invest'),
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
        verbose_name=_('Payout direct status'),
    )
    finished = models.BooleanField(
        verbose_name=_('Finished'),
    )
    # TODO: calculated_at default = now()
    calculated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    class Meta:
        db_table = 'invests'
        verbose_name = _('Invest')
        verbose_name_plural = _('Invests')

    def __str__(self):
        return str(self.user)
