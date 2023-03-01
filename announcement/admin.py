from django.contrib import admin

from .models import Announcement

# Register your models here.


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Announcement._meta.get_fields()]


admin.site.register(Announcement, AnnouncementAdmin)
