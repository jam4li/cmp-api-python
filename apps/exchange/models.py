from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

from apps.users.models import User

# Create your models here.


class ExchangeParent(BaseModel):
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    PENDING = "pending"
    STATUS_CHOICES = (
        (REJECTED, _("Rejected")),
        (ACCEPTED, _("Accepted")),
        (PENDING, _("Pending")),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('Parent'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status'),
    )

    class Meta:
        verbose_name = _('Exchange parent')
        verbose_name_plural = _('Exchange parents')

    def __str__(self):
        return str(self.user)
