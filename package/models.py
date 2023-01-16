from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Packages(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Name'))
    price = models.DecimalField(max_digits=30, decimal_places=2, verbose_name=_('Price'))
    image = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Image'))
    summery = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Summery'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    fee = models.DecimalField(max_digits=30, decimal_places=2, verbose_name=_('Fee'))
    daily_profit = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name=_('Daily profit'))
    daily_profit_percent = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Daily profit percent'))
    profit_limit = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, verbose_name=_('Profit limit'))
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = _('Package')
        verbose_name_plural = _('Packages')

    def __str__(self):
        return self.name