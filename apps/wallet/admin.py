from django.contrib import admin

from .models import Wallet

# Register your models here.


class WalletAdmin(admin.ModelAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    search_fields = [
        'user__email',
    ]

    fields = (
        'user',
        'title',
        'type',
        'access_type',
        'balance',
        'blocked_amount',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Wallet, WalletAdmin)
