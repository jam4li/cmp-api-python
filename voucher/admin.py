from django.contrib import admin

from .models import Voucher

# Register your models here.


class VoucherAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Voucher._meta.get_fields()]


admin.site.register(Voucher, VoucherAdmin)
