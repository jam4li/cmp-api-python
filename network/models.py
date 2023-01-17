from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Users

# Create your models here.

class Networks(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name=_('User'))
    status = models.BooleanField(default=True, verbose_name=_('Status'))
    left_count = models.BigIntegerField(default=0, verbose_name=_('Left count'))
    right_count = models.BigIntegerField(default=0, verbose_name=_('Right count'))
    left_amount = models.DecimalField(max_digits=20, decimal_places=3, default=0.000, verbose_name=_('Left amount'))
    right_amount = models.DecimalField(max_digits=20, decimal_places=3, default=0.000, verbose_name=_('Right amount'))
    invest = models.DecimalField(max_digits=20, decimal_places=3, default=0.000, verbose_name=_('Invest'))
    last_invest = models.DecimalField(max_digits=20, decimal_places=3, default=0.000, verbose_name=_('Last invest'))
    network_profit_daily_limit = models.DecimalField(max_digits=20, decimal_places=3, default=0.000, verbose_name=_('Network profit daily limit'))
    network_profit = models.DecimalField(max_digits=20, decimal_places=3, default=0.000, verbose_name=_('Network profit'))
    # TODO: referrer
    network_calculate_date = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = _('Network')
        verbose_name_plural = _('Networks')

    def __str__(self):
        return self.user