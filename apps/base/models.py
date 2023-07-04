from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Updated at'),
    )

    class Meta:
        abstract = True
