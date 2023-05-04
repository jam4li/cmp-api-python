from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

from apps.users.models import User
from apps.network.models import Network

# Create your models here.


class Referral(BaseModel):
    RIGHT = "right"
    LEFT = "left"
    RECRUITED_CHOICES = (
        (RIGHT, _("Right")),
        (LEFT, _("Left")),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name=_('User'),
    )
    network = models.ForeignKey(
        Network,
        on_delete=models.CASCADE,
        verbose_name=_('Network'),
    )
    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='referrer',
        verbose_name=_('Referrer'),
    )
    recruited = models.CharField(
        max_length=10,
        choices=RECRUITED_CHOICES,
        verbose_name=_('Recruited')
    )
    binary_place = models.CharField(
        max_length=500,
        verbose_name=_('Binary place'),
    )

    class Meta:
        verbose_name = _('Referral')
        verbose_name_plural = _('Referrals')

    def __str__(self):
        return str(self.user)
