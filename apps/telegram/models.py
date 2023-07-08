from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel, BaseAsyncSingletonModel
# Create your models here.


class TelegramConfig(BaseAsyncSingletonModel):
    support_username = models.CharField(
        max_length=255,
        verbose_name=_('Support username')
    )

    class Meta:
        verbose_name = _('Config')
        verbose_name_plural = _('Config')

    def __str__(self):
        return 'Primary Config'


class TelegramLanguage(BaseModel):
    ENGLISH = "en"
    ARABIC = "ar"
    PERSIAN = "fa"
    TURKISH = "tr"
    RUSSIAN = "ru"
    LANGUAGE_CODE_CHOICES = (
        (ENGLISH, _("English")),
        (ARABIC, _("Arabic")),
        (PERSIAN, _("Persian")),
        (TURKISH, _("Turkish")),
        (RUSSIAN, _("Russian")),
    )

    language_code = models.CharField(
        choices=LANGUAGE_CODE_CHOICES,
        max_length=4,
        verbose_name=_('Language code'),
    )

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    def __str__(self):
        return self.get_language_code_display()


def get_default_language():
    return TelegramLanguage.objects.get(language_code='en')


class TelegramUser(BaseModel):
    user_id = models.CharField(
        max_length=255,
        verbose_name=_('User id'),
    )
    language = models.ForeignKey(
        TelegramLanguage,
        on_delete=models.SET_DEFAULT,
        default=get_default_language,
    )

    class Meta:
        verbose_name = _('Telegram User')
        verbose_name_plural = _('Telegram Users')

    def __str__(self):
        return self.user_id


class TelegramNews(BaseModel):
    language = models.ForeignKey(
        TelegramLanguage,
        on_delete=models.CASCADE,
        verbose_name=_('Language'),
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

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')

    def __str__(self):
        return self.title


class TelegramNewsFile(BaseModel):
    file = models.FileField(
        upload_to='telegram/',
        blank=True,
        null=True,
        verbose_name=_('File'),
    )
    news = models.ForeignKey(
        TelegramNews,
        on_delete=models.CASCADE,
        verbose_name=_('News'),
    )

    class Meta:
        verbose_name = _('News file')
        verbose_name_plural = _('News files')

    def __str__(self):
        return str(self.file)


class TelegramEducate(BaseModel):
    language = models.ForeignKey(
        TelegramLanguage,
        on_delete=models.CASCADE,
        verbose_name=_('Language'),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )

    class Meta:
        verbose_name = _('Educate')
        verbose_name_plural = _('Educates')

    def __str__(self):
        return self.name


class TelegramEducateContent(BaseModel):
    educate = models.ForeignKey(
        TelegramEducate,
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
        upload_to='telegram/educate/',
        blank=True,
        null=True,
        verbose_name=_('File'),
    )

    class Meta:
        verbose_name = _('Educate content')
        verbose_name_plural = _('Educate contents')

    def __str__(self):
        return self.description


class TelegramOffice(BaseModel):
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
    )
    location_latitude = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )
    location_longitude = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )
    location_address = models.TextField(
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Office')
        verbose_name_plural = _('Offices')

    def __str__(self):
        return self.title


class TelegramOfficeFile(BaseModel):
    file = models.FileField(
        upload_to='telegram/office/',
        blank=True,
        null=True,
        verbose_name=_('File'),
    )
    office = models.ForeignKey(
        TelegramOffice,
        on_delete=models.CASCADE,
        verbose_name=_('Office'),
    )

    class Meta:
        verbose_name = _('Office file')
        verbose_name_plural = _('Office files')

    def __str__(self):
        return str(self.file)


class TelegramFAQ(BaseModel):
    language = models.ForeignKey(
        TelegramLanguage,
        on_delete=models.CASCADE,
        verbose_name=_('Language'),
    )
    question = models.CharField(
        max_length=100,
        verbose_name=_('Question'),
    )
    answer = models.TextField(
        max_length=500,
        verbose_name=_('Answer'),
    )

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')

    def __str__(self):
        return self.question
