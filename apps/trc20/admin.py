from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import Trc20

# Register your models here.


class Trc20Admin(BaseAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    search_fields = [
        'user__email',
        'address',
        'payment_txid',
    ]

    fields = (
        'user',
        'purchase',
        'message',
        'invoice_id',
        'merchant_id',
        'total_amount',
        'paid_amount',
        'address',
        'url',
        'symbol',
        'status',
        'payment_txid',
        'payment_confirmation',
        'expired_at',
    ) + BaseAdmin.fields

    list_display = [
        'user',
        'address',
        'payment_txid',
    ]

    readonly_fields = (
        'expired_at',
    ) + BaseAdmin.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Trc20, Trc20Admin)
