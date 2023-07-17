from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.base.admin import BaseAdmin

from .models import User, UserProfile, AdminProfile
from apps.package.models import Package

# Register your models here.


class UserProfileForm(forms.ModelForm):
    user_email = forms.EmailField(label='Email', max_length=255)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.initial['user_email'] = self.instance.user.email


class UserProfileAdmin(BaseAdmin):
    form = UserProfileForm
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
        'user_email',
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
    ) + BaseAdmin.fields

    readonly_fields = (
        'user_id',
        'user',
        'username',
        'referrer_code',
    ) + BaseAdmin.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs

    def user_id(self, obj):
        return obj.user.id

    def save_model(self, request, obj, form, change):
        obj.user.email = form.cleaned_data['user_email']
        obj.user.save()
        super().save_model(request, obj, form, change)


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
