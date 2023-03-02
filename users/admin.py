from django.contrib import admin

from .models import User, Admin

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.get_fields()]


admin.site.register(User, UserAdmin)


class AdminsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Admin._meta.get_fields()]


admin.site.register(Admin, AdminsAdmin)
