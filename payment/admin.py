from django.contrib import admin

from .models import Payment

# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.get_fields()]


admin.site.register(Payment, PaymentAdmin)
