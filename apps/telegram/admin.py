from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import (
    TelegramConfig,
    TelegramLanguage,
    TelegramUser,
    TelegramNewsFile,
    TelegramNews,
    TelegramEducate,
    TelegramEducateContent,
    TelegramOfficeFile,
    TelegramOffice,
    TelegramFAQ,
)

# Register your models here.


class TelegramLanguageAdmin(BaseAdmin):
    fields = (
        'language_code',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields


admin.site.register(TelegramLanguage, TelegramLanguageAdmin)


class TelegramUserAdmin(BaseAdmin):
    model = TelegramUser
    fields = (
        'user_id',
        'language',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields


admin.site.register(TelegramUser, TelegramUserAdmin)


class TelegramNewsFileInline(admin.TabularInline):
    model = TelegramNewsFile
    fields = (
        'file',
    )
    extra = 1


class TelegramNewsAdmin(BaseAdmin):
    fields = (
        'language',
        'title',
        'description',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields

    inlines = [
        TelegramNewsFileInline,
    ]


admin.site.register(TelegramNews, TelegramNewsAdmin)


class TelegramEducateContentInline(admin.TabularInline):
    model = TelegramEducateContent
    fields = (
        'title',
        'description',
        'file',
    )
    extra = 1


class TelegramEducateAdmin(BaseAdmin):
    fields = (
        'language',
        'name',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields

    inlines = [
        TelegramEducateContentInline,
    ]

    def last_5_titles(self, obj):
        titles = obj.telegrameducatecontent_set.order_by(
            '-id',
        )[:5].values_list('title', flat=True)
        return ", ".join(titles)

    list_display = (
        'name',
        'last_5_titles',
        'language',
    )


admin.site.register(TelegramEducate, TelegramEducateAdmin)


class TelegramOfficeFileInline(admin.TabularInline):
    model = TelegramOfficeFile
    fields = (
        'file',
    )
    extra = 1


class TelegramOfficeAdmin(BaseAdmin):
    fields = (
        'title',
        'location_latitude',
        'location_longitude',
        'location_address',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields

    inlines = [
        TelegramOfficeFileInline,
    ]


admin.site.register(TelegramOffice, TelegramOfficeAdmin)


class TelegramFAQAdmin(BaseAdmin):
    fields = (
        'language',
        'question',
        'answer',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields


admin.site.register(TelegramFAQ, TelegramFAQAdmin)


class TelegramConfigAdmin(BaseAdmin):
    fields = (
        'support_username',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields


admin.site.register(TelegramConfig, TelegramConfigAdmin)
