from django.utils.translation import gettext_lazy as _

from base.models import models, BaseModel

# Create your models here.


class Config(BaseModel):
    key = models.CharField(max_length=255, verbose_name=_('Key'))
    value = models.CharField(max_length=500, verbose_name=_('Value'))

    class Meta:
        db_table = 'configs'
        verbose_name = _('Config')
        verbose_name_plural = _('Configs')

    def __str__(self):
        return self.key
