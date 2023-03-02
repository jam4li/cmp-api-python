from django.contrib import admin

from .models import Transaction

# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transaction._meta.get_fields()]


admin.site.register(Transaction, TransactionAdmin)
