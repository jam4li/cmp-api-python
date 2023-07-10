from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

from apps.users.models import User
from apps.package.models import Package

# Create your models here.


class Purchase(BaseModel):
    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed"
    STATUS_CHOICES = (
        (SUCCESS, _("Success")),
        (PENDING, _("Pending")),
        (FAILED, _("Failed")),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        verbose_name=_('Package'),
        blank=True,
        null=True,
    )
    tether_amount = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('Tether amount'),
    )
    token_amount = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('Token amount'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )

    class Meta:
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')

    def __str__(self):
        return str(self.user)
