from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import Package

# Register your models here.


class PackageAdmin(BaseAdmin):
    search_fields = [
        'name',
    ]

    list_display = [
        'name',
        'price',
        'sort'
    ]

    fields = (
        'name',
        'price',
        'image',
        'sort',
        'summary',
        'status',
        'fee',
        'daily_profit',
        'daily_profit_percent',
        'profit_limit',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields


admin.site.register(Package, PackageAdmin)
