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
        'parent__user',
    ]

    fields = (
        'user',
        'parent',
        'status',
    )

    list_display = [
        'user',
        'parent',
        'status',
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(ExchangeParent, ExchangeParentAdmin)
