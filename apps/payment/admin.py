from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import Payment

# Register your models here.


class PaymentAdmin(BaseAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    search_fields = [
        'user__email',
        'payment_hash',
        'payment_code',
    ]

    fields = (
        'user',
        'amount',
        'payment_hash',
        'payment_code',
        'status',
        'symbol',
        'charge',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Payment, PaymentAdmin)
