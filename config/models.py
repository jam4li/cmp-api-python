from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Configs(models.Model):
    key = models.CharField(max_length=255, verbose_name=_('Key'))
    value = models.CharField(max_length=500, verbose_name=_('Value'))
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = _('Config')
        verbose_name_plural = _('Configs')

    def __str__(self):
        return self.key