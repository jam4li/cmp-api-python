from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Announcements(models.Model):
    PUBLISH = "publish"
    DRAFT = "draft"
    STATUS_CHOICES = (
        (PUBLISH, _("Publish")),
        (DRAFT, _("Draft")),
    )

    title = models.CharField(max_length=255, verbose_name=_('Title'))
    author = models.CharField(max_length=255, verbose_name=_('Author'))
    image = models.CharField(max_length=255, verbose_name=_('Image'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name=_('Status'))
    summery = models.TextField(max_length=500, verbose_name=_('Summery'))
    text = models.TextField(max_length=1000, verbose_name=_('Text'))
    publish_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')

    def __str__(self):
        return self.title
