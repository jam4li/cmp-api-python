from django.contrib import admin

from .models import Wallet

# Register your models here.


class WalletAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Wallet._meta.get_fields()]


admin.site.register(Wallet, WalletAdmin)
