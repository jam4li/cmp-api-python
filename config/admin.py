from django.contrib import admin

from .models import Config

# Register your models here.


class ConfigAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Config._meta.get_fields()]


admin.site.register(Config, ConfigAdmin)
