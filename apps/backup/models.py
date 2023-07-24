from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

# Create your models here.


class Backup(BaseModel):
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    STATUS_CHOICES = (
        (SUCCESS, _("Success")),
        (FAILED, _("Failed")),
        (IN_PROGRESS, _("In progress"))
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress",
        verbose_name=_('Status'),
    )

    class Meta:
        verbose_name = _('Backup')
        verbose_name_plural = _('Backups')

    def __str__(self):
        return self.name
