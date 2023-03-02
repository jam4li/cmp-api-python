from django.contrib import admin

from .models import CMPToken

# Register your models here.


class CMPTokenAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CMPToken._meta.get_fields()]


admin.site.register(CMPToken, CMPTokenAdmin)
