from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import Purchase

# Register your models here.


class PurchaseAdmin(BaseAdmin):
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
        'package',
        'tether_amount',
        'token_amount',
        'status',
    ) + BaseAdmin.fields

    list_display = [
        'user',
        'package',
        'status',
    ]

    readonly_fields = BaseAdmin.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Purchase, PurchaseAdmin)
