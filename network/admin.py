from django.contrib import admin

from .models import Networks

# Register your models here.


class NetworksAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Networks._meta.get_fields()]


admin.site.register(Networks, NetworksAdmin)
