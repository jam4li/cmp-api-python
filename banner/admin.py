from django.contrib import admin

from .models import Banner

# Register your models here.


class BannerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Banner._meta.get_fields()]


admin.site.register(Banner, BannerAdmin)
