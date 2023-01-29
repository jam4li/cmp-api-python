from django.contrib import admin

from .models import Withdraws

# Register your models here.


class WithdrawsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Withdraws._meta.get_fields()]


admin.site.register(Withdraws, WithdrawsAdmin)
