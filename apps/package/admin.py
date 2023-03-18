from django.contrib import admin

from .models import Package

# Register your models here.


class PackageAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]


admin.site.register(Package, PackageAdmin)
