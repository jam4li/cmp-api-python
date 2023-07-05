from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import ExchangeParent

# Register your models here.


class ExchangeParentAdmin(BaseAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    autocomplete_fields = [
        'parent',
    ]
    search_fields = [
        'user__email',
        'parent__user__email',
    ]

    fields = (
        'user',
        'parent',
        'status',
    ) + BaseAdmin.fields

    list_display = [
        'user',
        'parent',
        'status',
    ]

    readonly_fields = BaseAdmin.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(ExchangeParent, ExchangeParentAdmin)
