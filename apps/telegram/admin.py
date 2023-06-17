from django.contrib import admin

from .models import Educate, EducateContent

# Register your models here.


class EducateContentInline(admin.TabularInline):
    model = EducateContent
    extra = 1


class EducateAdmin(admin.ModelAdmin):
    fields = (
        'name',
    )

    inlines = [
        EducateContentInline,
    ]


admin.site.register(Educate, EducateAdmin)
