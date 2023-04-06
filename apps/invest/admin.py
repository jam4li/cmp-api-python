from django.contrib import admin

from .models import Invest

# Register your models here.


class InvestAdmin(admin.ModelAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    autocomplete_fields = [
        'package',
    ]
    search_fields = [
        'user__email',
        'package__name',
    ]

    fields = (
        'user',
        'package',
        'invest',
        'total_invest',
        'profit',
        'payout_binary_status',
        'payout_direct_status',
        'finished',
        'calculated_at',
        'deleted_at',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Invest, InvestAdmin)
