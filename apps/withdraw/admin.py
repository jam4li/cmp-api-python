from django.contrib import admin

from .models import Withdraw

# Register your models here.


class WithdrawAdmin(admin.ModelAdmin):
    list_select_related = True
    list_per_page = 50
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
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Withdraw, WithdrawAdmin)
