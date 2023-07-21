from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import ConfigWithdraw

# Register your models here.


class ConfigWithdrawAdmin(BaseAdmin):
    fields = (
        'is_active',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        count = ConfigWithdraw.objects.count()
        if count == 0:
            self.message_user(
                request,
                "No Configuration found. A new Configuration will be created automatically on save.",
                level='info',
            )
        elif count > 1:
            self.message_user(
                request,
                "Warning: Multiple Configurations found. Only one Configuration instance is allowed.",
                level='warning',
            )
        return super().changelist_view(request, extra_context)


admin.site.register(ConfigWithdraw, ConfigWithdrawAdmin)
