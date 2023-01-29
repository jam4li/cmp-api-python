from django.contrib import admin

from .models import Wallets

# Register your models here.


class WalletsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Wallets._meta.get_fields()]


admin.site.register(Wallets, WalletsAdmin)
