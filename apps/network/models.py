from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

from apps.users.models import User
from apps.package.models import Package

# Create your models here.


class Network(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='network_user',
        verbose_name=_('User'),
    )
    status = models.BooleanField(
        default=True,
        verbose_name=_('Status'),
    )
    left_count = models.BigIntegerField(
        default=0,
        verbose_name=_('Left count'),
    )
    right_count = models.BigIntegerField(
        default=0,
        verbose_name=_('Right count'),
    )
    left_amount = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Left amount'),
    )
    right_amount = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Right amount'),
    )
    invest = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Invest'),
    )
    last_invest = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Last invest'),
    )
    network_profit_daily_limit = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Network profit daily limit'),
    )
    network_profit = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Network profit'),
    )
    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='network_referrer',
        verbose_name=_('Referrer'),
    )
    network_calculate_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Network')
        verbose_name_plural = _('Networks')

    def __str__(self):
        return str(self.user)
