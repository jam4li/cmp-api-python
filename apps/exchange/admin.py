from django.contrib import admin

from .models import ExchangeParent

# Register your models here.


class ExchangeParentAdmin(admin.ModelAdmin):
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
        'created_at',
        'updated_at',
    )

    list_display = [
        'user',
        'parent',
        'status',
    ]

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(ExchangeParent, ExchangeParentAdmin)
