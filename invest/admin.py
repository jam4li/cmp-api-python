from django.contrib import admin

from .models import Invests

# Register your models here.


class InvestsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Invests._meta.get_fields()]


admin.site.register(Invests, InvestsAdmin)
