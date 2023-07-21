# signals.py

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ConfigWithdraw


@receiver(pre_save, sender=ConfigWithdraw)
def enforce_singleton(sender, instance, **kwargs):
    if ConfigWithdraw.objects.exists() and not instance.pk:
        raise ValidationError("Only one Configuration instance is allowed.")
