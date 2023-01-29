from django.contrib import admin

from .models import Configs

# Register your models here.


class ConfigfsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Configs._meta.get_fields()]


admin.site.register(Configs, ConfigfsAdmin)
