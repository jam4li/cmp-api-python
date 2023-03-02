from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User

# Create your models here.


class Payment(models.Model):
    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed"
    STATUS_CHOICES = (
        (SUCCESS, _("Success")),
        (PENDING, _("Pending")),
        (FAILED, _("Failed")),
    )

    USDT = "USDT"
    CMP = "CMP"
    SYMBOL_CHOICES = (
        (USDT, _("Usdt")),
        (CMP, _("Cmp")),
    )

    payment_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Payment hash'),
    )
    payment_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Payment code'),
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        verbose_name=_('Amount'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )
    symbol = models.CharField(
        max_length=10,
        choices=SYMBOL_CHOICES,
        verbose_name=_('Symbol'),
    )
    charge = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('Charge'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    class Meta:
        db_table = 'payments'
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return self.payment_hash
