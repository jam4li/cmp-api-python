from django.contrib import admin

from .models import Vouchers

# Register your models here.


class VouchersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Vouchers._meta.get_fields()]


admin.site.register(Vouchers, VouchersAdmin)
