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


admin.site.register(Package, PackageAdmin)
