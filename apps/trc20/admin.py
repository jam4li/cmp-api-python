from django.contrib import admin

from .models import Trc20

# Register your models here.


class Trc20Admin(admin.ModelAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    search_fields = [
        'user__email',
        'address',
    ]

    fields = (
        'user',
        'message',
        'invoice_id',
        'total_amount',
        'paid_amount',
        'address',
        'symbol',
        'status',
    )

    list_display = [
        'user',
        'address',
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Trc20, Trc20Admin)
