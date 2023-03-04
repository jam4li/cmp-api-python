from django.utils.translation import gettext_lazy as _

from base.models import models, BaseModel

from users.models import User
from package.models import Package

# Create your models here.


class Network(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='network_user',
        verbose_name=_('User'),
    )
    status = models.BooleanField(
        default=True,
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
    invest = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0.000,
        verbose_name=_('Invest'),
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
        related_name='network_referrer',
        verbose_name=_('Referrer'),
    )
    network_calculate_date = models.DateTimeField()

    class Meta:
        db_table = 'networks'
        verbose_name = _('Network')
        verbose_name_plural = _('Networks')

    def __str__(self):
        return self.user


class NetworkTreeTransfer(BaseModel):
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
        related_name='origin_user',
        verbose_name=_('Origin user'),
    )
    endpoint_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='endpoint_user',
        verbose_name=_('Endpoint user'),
    )
    origin_binary_place = models.CharField(
        max_length=255,
        verbose_name=_('Origin binary place'),
    )
    endpoint_binary_place = models.CharField(
        max_length=255,
        verbose_name=_('Endpoint binary place'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status'),
    )
    side = models.CharField(
        max_length=10,
        choices=SIDE_CHOICES,
        verbose_name=_('Side'),
    )
    remove_user_all_invests = models.BooleanField(
        default=False,
        verbose_name=_('Remove user all invests'),
    )
    remove_user_invests_from_origin_tree = models.BooleanField(
        default=False,
        verbose_name=_('Remove user invests from origin tree'),
    )
    add_user_invests_to_endpoint_tree = models.BooleanField(
        default=False,
        verbose_name=_('Add user invests to endpoint tree'),
    )

    class Meta:
        db_table = 'transfer_network_tree_processes'
        verbose_name = _('Network tree transfer')
        verbose_name_plural = _('Network tree transfers')

    def __str__(self):
        return str(self.id)


class NetworkTreeTransferred(BaseModel):
    # network_tree_transfer is transfer_network_tree_processes
    # in the previous class
    network_tree_transfer = models.ForeignKey(
        NetworkTreeTransfer,
        on_delete=models.CASCADE,
        verbose_name=_('Network tree transfer'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    last_package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Last package'),
    )
    origin_binary_place = models.CharField(
        max_length=255,
        verbose_name=_('Origin binary place'),
    )
    endpoint_binary_place = models.CharField(
        max_length=255,
        verbose_name=_('Endpoint binary place'),
    )
    invest = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )
    last_invest = models.DecimalField(
        max_digits=30,
        decimal_places=10,
    )
    is_head = models.BooleanField(
        default=False,
        verbose_name=_('Is head'),
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'transferred_network_trees'
        verbose_name = _('Network tree transferred')
        verbose_name_plural = _('Network tree transferred')

    def __str__(self):
        return str(self.user)
