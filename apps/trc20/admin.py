from django.contrib import admin

from .models import Trc20

# Register your models here.


class Trc20Admin(admin.ModelAdmin):
    list_display = [field.name for field in Trc20._meta.get_fields()]


admin.site.register(Trc20, Trc20Admin)
