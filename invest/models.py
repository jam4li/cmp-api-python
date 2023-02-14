from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Users
from package.models import Packages

# Create your models here.


class Invests(models.Model):
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    package = models.ForeignKey(
        Packages,
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
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )
    deleted_at = models.DateTimeField()

    class Meta:
        verbose_name = _('Invest')
        verbose_name_plural = _('Invests')

    def __str__(self):
        return self.user
