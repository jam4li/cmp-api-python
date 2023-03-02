from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from package.models import Package

# Create your models here.


class User(AbstractUser):
    USER = "user"
    ADMIN = "admin"
    ROLE_CHOICES = (
        (USER, _("User")),
        (ADMIN, _("Admin")),
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Package'),
    )
    # TODO: Add referrer_id
    email = models.CharField(
        max_length=255,
        verbose_name=_('Email'),
    )
    ex_email = models.CharField(
        max_length=255,
        verbose_name=_('Ex email'),
    )
    referrer_code = models.CharField(
        max_length=255,
        verbose_name=_('Referrer code'),
    )
    status = models.BooleanField(
        default=True,
        verbose_name=_('Status'),
    )
    enable_google_2fa_verification = models.BooleanField(
        default=False,
        verbose_name=_('Enable google 2fa'),
    )
    google_2fa_secret = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Google 2fa secret'),
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )
    avatar = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Avatar'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        verbose_name=_('Role'),
    )
    trc20_withdraw_wallet = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('TRC20 withdraw wallet'),
    )
    weekly_withdraw_amount = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name=_('Weekly withdraw amount'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email


class Admin(models.Model):
    ADMIN = "admin"
    ACCOUNTING = "accounting"
    SUPPORT = "support"
    ROLE_CHOICES = (
        (ADMIN, _("Admin")),
        (ACCOUNTING, _("Accounting")),
        (SUPPORT, _("Support")),
    )

    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )
    email = models.CharField(
        max_length=255,
        verbose_name=_('Email'),
    )
    enable_google_2fa_verification = models.BooleanField(
        verbose_name=_('Enable google 2fa verification'),
    )
    google_2fa_s = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Google 2fa'),
    )
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        verbose_name=_('Role'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    class Meta:
        db_table = 'admins'
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')

    def __str__(self):
        return self.email
