from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

# Create your models here.


class Banner(BaseModel):
    big_title = models.CharField(
        max_length=255,
        verbose_name=_('Big title'),
    )
    small_title = models.CharField(
        max_length=255,
        verbose_name=_('Small title'),
    )
    sort = models.IntegerField(
        verbose_name=_('Sort'),
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to='banner/',
        null=True,
        blank=True,
        verbose_name=_('Image'),
    )

    class Meta:
        db_table = 'banners'
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')

    def __str__(self):
        return self.small_title
