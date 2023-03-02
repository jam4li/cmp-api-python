from django.contrib import admin

from .models import Withdraw

# Register your models here.


class WithdrawsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Withdraw._meta.get_fields()]


admin.site.register(Withdraw, WithdrawsAdmin)
