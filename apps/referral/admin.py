from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import Referral

# Register your models here.


class ReferralAdmin(BaseAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
        'referrer',
    )
    autocomplete_fields = [
        'network',
    ]
    search_fields = [
        'user__email',
        'referrer__email',
    ]

    fields = (
        'user',
        'network',
        'referrer',
        'recruited',
        'binary_place',
    ) + BaseAdmin.fields

    readonly_fields = (
        'user',
        'network',
        'binary_place',
    ) + BaseAdmin.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(Referral, ReferralAdmin)
