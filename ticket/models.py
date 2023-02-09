from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Users


# Create your models here.

class TicketDepartment(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_('Name'),
    )
    icon = models.ImageField(
        upload_to='ticket/department/',
        verbose_name=_('Icon'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active'),
    )

    class Meta:
        verbose_name = _('Ticket department')
        verbose_name_plural = _('Ticket departments')

    def __str__(self):
        return self.name


class Ticket(models.Model):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    IMPORTANT_LEVEL_CHOICES = (
        (HIGH, _("High")),
        (MEDIUM, _("Medium")),
        (LOW, _("Low")),
    )

    CLOSE = "close"
    OPEN = "open"
    PENDING = "pending"
    TICKET_STATUS_CHOICES = (
        (CLOSE, _("Close")),
        (OPEN, _("Open")),
        (PENDING, _("Pending")),
    )

    # User should be set from self.request.user
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    department = models.ForeignKey(
        TicketDepartment,
        on_delete=models.CASCADE,
        verbose_name=_('Department'),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
    )
    content = models.TextField(
        max_length=255,
        verbose_name=_('Content'),
    )
    # I think attachments on the laravel side was multiple
    attachments = models.FileField(
        upload_to='ticket/attachments/',
        blank=True,
        null=True,
        verbose_name=_('Attachments'),
    )
    important_level = models.CharField(
        max_length=10,
        choices=IMPORTANT_LEVEL_CHOICES,
        default='medium',
        verbose_name=_('Important level'),
    )
    # TODO: If status has been changed to close, and a reply submits,
    # the status should be changed to open
    status = models.CharField(
        max_length=10,
        choices=TICKET_STATUS_CHOICES,
        default="open",
        verbose_name=_('Status'),
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
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    def __str__(self):
        return self.name


class TicketReply(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        verbose_name=_('Ticket'),
    )
    content = models.TextField(
        max_length=255,
        verbose_name=_('Content'),
    )
    attachments = models.FileField(
        upload_to='ticket/attachments/',
        blank=True,
        null=True,
        verbose_name=_('Attachments'),
    )

    class Meta:
        verbose_name = _('Ticket reply')
        verbose_name_plural = _('Ticket replies')

    def __str__(self):
        return str(self.ticket)
