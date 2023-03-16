from django.contrib import admin

from .models import User, UserProfile, AdminProfile
from apps.package.models import Package

# Register your models here.


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 0


class AdminProfileInline(admin.TabularInline):
    model = AdminProfile
    extra = 0


class UserAdmin(admin.ModelAdmin):
    fields = (
        'email',
        'name',
        'enable_google_2fa_verification',
        'google_2fa_secret',
    )

    inlines = [
        UserProfileInline,
        AdminProfileInline,
    ]


admin.site.register(User, UserAdmin)
