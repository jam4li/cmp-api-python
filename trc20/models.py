from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Trc20(models.Model):
    PENDING = 0
    PAID = 1
    FAILED = 3
    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (PAID, _("Paid")),
        (FAILED, _("Failed")),
    )

    invoice_id = models.CharField(
        max_length=20,
        verbose_name=_('Invoice id'),
    )
    amount = models.FloatField(
        verbose_name=_('Amount'),
    )
    payment_code = models.CharField(
        max_length=50,
        verbose_name=_('Payment code'),
    )
    user_id = models.CharField(
        max_length=20,
        verbose_name=_('User id'),
    )
    symbol = models.CharField(
        max_length=20,
        verbose_name=_('Symbol'),
    )
    callback_url = models.CharField(
        max_length=100,
        verbose_name=_('Callback url'),
    )
    status = models.SmallIntegerField(
        default=0,
        choices=STATUS_CHOICES,
        verbose_name=_('Status'),
    )

    class Meta:
        verbose_name = _('Trc20')
        verbose_name_plural = _('Trc20')

    def __str__(self):
        return self.invoice_id
