from django.contrib import admin

from .models import Network

# Register your models here.


class NetworkAdmin(admin.ModelAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
        'referrer',
    )
    search_fields = [
        'user__email',
        'referrer__email',
    ]

    fields = (
        'user',
        'status',
        'left_count',
        'right_count',
        'left_amount',
        'right_amount',
        'invest',
        'last_invest',
        'network_profit_daily_limit',
        'network_profit',
        'referrer',
        'network_calculate_date',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Network, NetworkAdmin)
