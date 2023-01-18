from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class ExchangeParent(models.Model):
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    PENDING = "pending"
    STATUS_CHOICES = (
        (REJECTED, _("Rejected")),
        (ACCEPTED, _("Accepted")),
        (PENDING, _("Pending")),
    )

    user_email = models.CharField(max_length=50, verbose_name=_('User'))
    parent = models.CharField(max_length=50, verbose_name=_('Parent'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name=_('Status'))

    class Meta:
        verbose_name = _('Exchange parent')
        verbose_name_plural = _('Exchange parents')

    def __str__(self):
        return self.user_email
