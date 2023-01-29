from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Banners(models.Model):
    big_title = models.CharField(max_length=255, verbose_name=_('Big title'))
    small_title = models.CharField(max_length=255, verbose_name=_('Small title'))
    sort = models.IntegerField(verbose_name=_('Sort'), null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')

    def __str__(self):
        return self.small_title