from django.contrib import admin
from django.template.defaultfilters import date as admin_dateformat

# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    def custom_created_at(self, obj):
        return admin_dateformat(obj.created_at, 'Y-m-d H:i:s')

    def custom_updated_at(self, obj):
        return admin_dateformat(obj.updated_at, 'Y-m-d H:i:s')

    fields = (
        'id',
        'custom_created_at',
        'custom_updated_at',
    )

    readonly_fields = (
        'id',
        'custom_created_at',
        'custom_updated_at',
    )
