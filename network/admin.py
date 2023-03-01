from django.contrib import admin

from .models import Network

# Register your models here.


class NetworkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Network._meta.get_fields()]


admin.site.register(Network, NetworkAdmin)
