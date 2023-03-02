from django.contrib import admin

from .models import Referral

# Register your models here.


class ReferralAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Referral._meta.get_fields()]


admin.site.register(Referral, ReferralAdmin)
