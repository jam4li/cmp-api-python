from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import Transaction

# Register your models here.


class TransactionAdmin(BaseAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    autocomplete_fields = [
        'withdraw',
        'payment',
    ]
    search_fields = [
        'user__email',
    ]

    fields = (
        'user',
        'withdraw',
        'payment',
        'amount',
        'type',
        'status',
        'description',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Transaction, TransactionAdmin)
