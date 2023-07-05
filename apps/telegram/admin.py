from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import Educate, EducateContent

# Register your models here.


class EducateContentInline(admin.TabularInline):
    model = EducateContent
    extra = 1


class EducateAdmin(BaseAdmin):
    fields = (
        'name',
    )

    inlines = [
        EducateContentInline,
    ]


admin.site.register(Educate, EducateAdmin)
