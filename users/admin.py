from django.contrib import admin

from .models import Users, Admins

# Register your models here.


admin.site.register(Users)


class AdminsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Admins._meta.get_fields()]


admin.site.register(Admins, AdminsAdmin)
