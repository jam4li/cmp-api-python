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
        'total_invest',
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
            total_invest = form.cleaned_data['total_invest']

            user_profile = UserProfile.objects.get(user=user)

            package_price = package.price

            network = Network.objects.get(user=user)

            # Calculate and update total_invest
            total_invest = 0
            total_invest += package.price
            invest_list = Invest.objects.filter(user=user)

            for invest in invest_list:
                total_invest += invest.invest

            network.invest = total_invest
            network.last_invest = package.price
            network.save()

            if user_profile.package:
                if package_price > user_profile.package.price:
                    user_profile.package = package
                    user_profile.save()

            else:
                user_profile.package = package
                user_profile.save()

            obj.invest = package.price
            obj.total_invest = total_invest
            obj.created_at = timezone.now()

        super().save_model(request, obj, form, change)


admin.site.register(Invest, InvestAdmin)
