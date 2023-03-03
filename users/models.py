from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

from package.models import Package

# Create your models here.


class User(AbstractUser):
    # Authentication
    username=None
    email = models.CharField(
        unique=True,
        max_length=255,
        verbose_name=_('Email'),
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Name'),
    )
    enable_google_2fa_verification = models.BooleanField(
        default=False,
        verbose_name=_('Enable google 2fa verification'),
    )
    google_2fa_secret = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Google 2fa'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    # Make first_name, last_name, date_joined nullable
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    date_joined = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    USER = "user"
    ADMIN = "admin"
    ROLE_CHOICES = (
        (USER, _("User")),
        (ADMIN, _("Admin")),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    username = models.CharField(
        max_length=255,
        verbose_name=_('Username'),
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Package'),
    )
    referrer = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Referrer'),
    )
    ex_email = models.CharField(
        max_length=255,
        blank=True,
        null=True,
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
    avatar = models.ImageField(
        upload_to='user/',
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
    weekly_withdraw_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Weekly withdraw date'),
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return str(self.user)


class AdminProfile(models.Model):
    ADMIN = "admin"
    ACCOUNTING = "accounting"
    SUPPORT = "support"
    ROLE_CHOICES = (
        (ADMIN, _("Admin")),
        (ACCOUNTING, _("Accounting")),
        (SUPPORT, _("Support")),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        verbose_name=_('Role'),
    )

    class Meta:
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')

    def __str__(self):
        return (self.user)
