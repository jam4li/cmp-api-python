from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import Backup

# Register your models here.


class BackupAdmin(BaseAdmin):
    fields = (
        'name',
        'status',
    ) + BaseAdmin.fields

    list_display = (
        'name',
        'status',
        'created_at',
    )

    readonly_fields = (
        'name',
        'status',
    ) + BaseAdmin.readonly_fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request):
        return False


admin.site.register(Backup, BackupAdmin)
