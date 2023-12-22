from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import Wallet

# Register your models here.


class WalletAdmin(BaseAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    search_fields = [
        'user__email',
    ]

    fields = (
        'is_checked',
        'user',
        'access_type',
        'balance',
        'blocked_amount',
        'title',
        'type',
    ) + BaseAdmin.fields

    list_display = [
        'user',
        'type',
        'balance',
        'is_checked',
    ]

    readonly_fields = (
        'title',
        'type',
    ) + BaseAdmin.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Wallet, WalletAdmin)
