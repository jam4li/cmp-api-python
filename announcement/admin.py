from django.contrib import admin

from .models import Announcements

# Register your models here.


class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Announcements._meta.get_fields()]


admin.site.register(Announcements, AnnouncementsAdmin)
