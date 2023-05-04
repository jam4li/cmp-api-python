from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

# Create your models here.


class Banner(BaseModel):
    PUBLISH = "publish"
    DRAFT = "draft"
    STATUS_CHOICES = (
        (PUBLISH, _("Publish")),
        (DRAFT, _("Draft")),
    )

    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
    )
    author = models.CharField(
        max_length=255,
        verbose_name=_('Author'),
    )
    image = models.ImageField(
        upload_to='banner',
        verbose_name=_('Image'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name=_('Status'),
    )
    summary = models.TextField(
        max_length=500,
        verbose_name=_('Summary'),
    )
    text = models.TextField(
        max_length=1000,
        verbose_name=_('Text'),
    )
    publish_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')

    def __str__(self):
        return self.title
