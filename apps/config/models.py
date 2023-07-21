from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

# Create your models here.


class ConfigManager(models.Manager):
    def get_instance(self):
        if self.count() == 0:
            return self.create()
        return self.first()


class ConfigWithdraw(BaseModel):
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('Is active'),
    )

    objects = ConfigManager()

    class Meta:
        verbose_name = _('Withdraw config')
        verbose_name_plural = _('Withdraw configs')

    def __str__(self):
        return 'Config'
