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
        'access_type',
        'balance',
        'blocked_amount',
        'title',
        'type',
        'created_at',
        'updated_at',
    )

    list_display = [
        'user',
        'type',
        'balance',
    ]

    readonly_fields = (
        'title',
        'type',
        'created_at',
        'updated_at',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Wallet, WalletAdmin)
