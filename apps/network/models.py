from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel

from apps.users.models import User
from apps.package.models import Package
from apps.invest.models import Invest

# Create your models here.


class Network(BaseModel):
    RIGHT = "right"
    LEFT = "left"
    SIDE_CHOICES = (
        (RIGHT, _("Right")),
        (LEFT, _("Left")),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='network_user',
        verbose_name=_('User'),
    )
    status = models.BooleanField(
        default=False,
        verbose_name=_('Status'),
    )
    left_count = models.BigIntegerField(
        default=0,
        verbose_name=_('Left count'),
    )
    right_count = models.BigIntegerField(
        default=0,
        verbose_name=_('Right count'),
    )
    left_amount = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Left amount'),
    )
    right_amount = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Right amount'),
    )
    total_active_invest = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Total active invest'),
    )
    total_all_invest = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Total all invest'),
    )
    last_invest = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Last invest'),
    )
    network_profit_daily_limit = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Network profit daily limit'),
    )
    network_profit = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Network profit'),
    )
    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='network_referrer',
        verbose_name=_('Referrer'),
    )
    side = models.CharField(
        max_length=10,
        choices=SIDE_CHOICES,
        verbose_name=_('Side')
    )
    binary_place = models.CharField(
        max_length=500,
        verbose_name=_('Binary place'),
    )
    network_calculate_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Network')
        verbose_name_plural = _('Networks')

    def __str__(self):
        return str(self.user)


class NetworkTransfer(BaseModel):
    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed"
    STATUS_CHOICES = (
        (SUCCESS, _("Success")),
        (PENDING, _("Pending")),
        (FAILED, _("Failed")),
    )

    LEFT = "left"
    RIGHT = "right"
    SIDE_CHOICES = (
        (LEFT, _("Left")),
        (RIGHT, _("Right")),
    )

    origin_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Origin user'),
        related_name='origin_transfers',
    )
    endpoint_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Endpoint user'),
        related_name='endpoint_transfers',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_('Status'),
    )
    side = models.CharField(
        max_length=10,
        choices=SIDE_CHOICES,
        verbose_name=_("Side"),
    )

    class Meta:
        verbose_name = _('Network transfer')
        verbose_name_plural = _('Network transfers')

    def __str__(self):
        return str(self.id)


class NetworkTransaction(BaseModel):
    BINARY = "binary"
    DIRECT = "direct"
    PROFIT = "profit"
    TYPE_CHOICES = (
        (BINARY, _("Binary")),
        (DIRECT, _("Direct")),
        (PROFIT, _("Profit")),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    invest = models.ForeignKey(
        Invest,
        on_delete=models.CASCADE,
        verbose_name=_('Invest'),
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name=_('Type'),
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        verbose_name=_('Amount'),
    )
    day = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Day'),
    )
    description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('Description'),
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Network transaction')
        verbose_name_plural = _('Network transactions')

    def __str__(self):
        return str(self.user)
