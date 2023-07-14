from django.contrib import admin
from django.utils import timezone
from django.template.defaultfilters import date as admin_dateformat

# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    def custom_created_at(self, obj):
        return admin_dateformat(obj.created_at, 'Y-m-d H:i:s')

    def custom_updated_at(self, obj):
        return admin_dateformat(obj.updated_at, 'Y-m-d H:i:s')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = timezone.now()
        obj.updated_at = timezone.now()

        super().save_model(request, obj, form, change)

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
