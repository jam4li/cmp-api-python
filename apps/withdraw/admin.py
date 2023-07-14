from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import Withdraw

# Register your models here.


class WithdrawAdmin(BaseAdmin):
    list_select_related = True
    list_per_page = 50

    custom_created_at = BaseAdmin.custom_created_at
    custom_updated_at = BaseAdmin.custom_updated_at

    raw_id_fields = (
        'user',
    )
    search_fields = [
        'user__email',
        'wallet_address',
        'transaction_hash',
    ]

    fields = (
        'user',
        'amount',
        'fee',
        'wallet_address',
        'transaction_hash',
        'status',
        'wallet_type',
    ) + BaseAdmin.fields

    list_display = [
        'user',
        'amount',
        'fee',
        'wallet_type',
        'wallet_address',
        'status',
        'custom_created_at',
        'custom_updated_at',
    ]

    readonly_fields = BaseAdmin.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Withdraw, WithdrawAdmin)
