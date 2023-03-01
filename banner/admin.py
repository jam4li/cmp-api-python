from django.contrib import admin

from .models import Banners

# Register your models here.


class BannerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Banners._meta.get_fields()]


admin.site.register(Banners, BannerAdmin)
