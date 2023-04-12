from django.contrib import admin

from .models import Transaction

# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
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
        'voucher',
        'cmp_token',
        'amount',
        'type',
        'status',
        'description',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Transaction, TransactionAdmin)
