import random
import string
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.base.admin import BaseAdmin

from .models import User, UserProfile, AdminProfile

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
        'referrer',
    ]
    search_fields = [
        'user__email',
        'username',
        'referrer__username',
    ]

    fields = (
        'user_id',
        'user',
        'username',
        'user_email',
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

    def delete_view(self, request, object_id, extra_context=None):
        user_profile = self.get_object(request, object_id)
        opts = self.model._meta
        app_label = opts.app_label

        if request.method == 'POST':
            # Generate a random 10 digits number in string
            random_string = ''.join(random.choices(string.digits, k=10))

            new_email = "deletedAccount" + random_string + "@cm-enterprise.net"
            previous_email = user_profile.user.email

            user_profile.user.email = new_email
            user_profile.ex_email = previous_email

            user_profile.user.save()
            user_profile.save()

            # Redirect to the change form view to show the updated data
            change_url = reverse(
                'admin:%s_%s_change' % (
                    user_profile._meta.app_label,
                    user_profile._meta.model_name,
                ),
                args=[user_profile.pk]
            )
            return HttpResponseRedirect(change_url)

        # Display the confirmation page for deletion
        context = {
            **self.admin_site.each_context(request),
            'title': 'Delete',
            'object_name': str(user_profile),
            'object': user_profile,
            'opts': opts,
            'app_label': app_label,
        }

        return self.render_delete_form(request, context)


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
