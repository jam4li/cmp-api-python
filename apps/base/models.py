from django.db import models
from django.utils import timezone
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


class BaseAsyncSingletonModelManager(models.Manager):
    async def get_or_create_singleton(self):
        try:
            instance = await self.aget(pk=1)
        except self.model.DoesNotExist:
            instance = await self.acreate(pk=1)
        return instance


class BaseAsyncSingletonModel(BaseModel):
    objects = BaseAsyncSingletonModelManager()

    class Meta:
        abstract = True
