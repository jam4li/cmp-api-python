from django.contrib import admin

from .models import Invest

# Register your models here.


class InvestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Invest._meta.get_fields()]


admin.site.register(Invest, InvestAdmin)
