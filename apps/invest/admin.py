from django.contrib import admin
from django.utils import timezone

from apps.base.admin import BaseAdmin

from .models import Invest
from apps.network.models import Network
from apps.users.models import User, UserProfile
from apps.package.models import Package

# Register your models here.


class InvestAdmin(BaseAdmin):
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
        'profit',
        'payout_binary_status',
        'payout_direct_status',
        'finished',
        'calculated_at',
        'deleted_at',
    ) + BaseAdmin.fields

    readonly_fields = (
        'calculated_at',
        'deleted_at',
    ) + BaseAdmin.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            user = form.cleaned_data['user']
            package = form.cleaned_data['package']

            user_profile = UserProfile.objects.get(user=user)

            package_price = package.price

            network = Network.objects.get(user=user)

            # Calculate and update total_active_invest
            total_active_invest = 0
            total_active_invest += package.price
            invest_list = Invest.objects.filter(user=user, finished=False)

            for invest in invest_list:
                total_active_invest += invest.invest

            network.total_active_invest = total_active_invest
            network.last_invest = package.price
            network.save()

            obj.invest = package.price
            obj.created_at = timezone.now()

        super().save_model(request, obj, form, change)


admin.site.register(Invest, InvestAdmin)
