from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile, AdminProfile
from apps.package.models import Package

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    autocomplete_fields = [
        'package',
        'referrer',
    ]
    search_fields = [
        'user__email',
        'username',
        'package__name',
        'referrer__username',
    ]

    fields = (
        'user_id',
        'user',
        'username',
        'package',
        'referrer',
        'ex_email',
        'referrer_code',
        'status',
        'avatar',
        'role',
        'trc20_withdraw_wallet',
        'weekly_withdraw_amount',
        'weekly_withdraw_date',
    )

    readonly_fields = (
        'user_id',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs

    def user_id(self, obj):
        return obj.user.id


admin.site.register(UserProfile, UserProfileAdmin)


class AdminProfileAdmin(admin.ModelAdmin):
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
        'role',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs


admin.site.register(AdminProfile, AdminProfileAdmin)
