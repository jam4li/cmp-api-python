from django.contrib import admin
from django.core.paginator import Paginator

from .models import Network, NetworkTransaction, NetworkTransfer

# Register your models here.


class NoCountPaginator(Paginator):
    @property
    def count(self):
        return 999999


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
        'created_at',
        'updated_at',
    )

    readonly_fields = (
        'network_calculate_date',
        'created_at',
        'updated_at',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Network, NetworkAdmin)


class NetworkTransferAdmin(admin.ModelAdmin):
    raw_id_fields = (
        'origin_user',
        'endpoint_user',
    )

    search_fields = [
        'origin_user__email',
        'origin_user__username',
        'endpoint_user__email',
        'endpoint_user__username'
    ]

    fields = (
        'origin_user',
        'endpoint_user',
        'status',
        'side',
        'created_at',
        'updated_at',
    )

    readonly_fields = (
        'status',
        'created_at',
        'updated_at',
    )


admin.site.register(NetworkTransfer, NetworkTransferAdmin)


class NetworkTransactionAdmin(admin.ModelAdmin):
    paginator = NoCountPaginator
    show_full_result_count = False

    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    autocomplete_fields = [
        'invest',
    ]
    search_fields = [
        'user__email',
        'invest__id',
    ]

    fields = (
        'user',
        'invest',
        'type',
        'amount',
        'day',
        'description',
        'deleted_at',
        'created_at',
        'updated_at',
    )

    readonly_fields = (
        'deleted_at',
        'created_at',
        'updated_at',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(NetworkTransaction, NetworkTransactionAdmin)
