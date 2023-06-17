from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel
# Create your models here.


class Educate(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )

    class Meta:
        verbose_name = _('Educate')
        verbose_name_plural = _('Educates')

    def __str__(self):
        return self.name


class EducateContent(BaseModel):
    educate = models.ForeignKey(
        Educate,
        on_delete=models.CASCADE,
        verbose_name=_('Educate'),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
    )
    description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('Description'),
    )
    file = models.FileField(
        upload_to='educate/',
        blank=True,
        null=True,
        verbose_name=_('File'),
    )

    class Meta:
        verbose_name = _('Educate content')
        verbose_name_plural = _('Educate contents')

    def __str__(self):
        return self.description
