from django.contrib import admin

from .models import User, Admin

# Register your models here.


admin.site.register(User)


class AdminsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Admin._meta.get_fields()]


admin.site.register(Admin, AdminsAdmin)
