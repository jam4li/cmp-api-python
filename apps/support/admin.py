from django.contrib import admin

from .models import SupportTicket, SupportDepartment, SupportTicketReply

# Register your models here.


class SupportTicketReplyInline(admin.TabularInline):
    model = SupportTicketReply
    extra = 1


class SupportTicketAdmin(admin.ModelAdmin):
    list_select_related = True
    list_per_page = 50
    raw_id_fields = (
        'user',
    )
    autocomplete_fields = [
        'department',
    ]
    search_fields = [
        'user__email',
        'department__name',
    ]

    fields = (
        'user',
        'department',
        'title',
        'content',
        'attachments',
        'important_level',
        'status',
    )

    inlines = [
        SupportTicketReplyInline,
    ]

    list_display = [
        'user',
        'department',
        'title',
    ]


admin.site.register(SupportTicket, SupportTicketAdmin)


class SupportDepartmentAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'icon',
        'is_active',
    )


admin.site.register(SupportDepartment, SupportDepartmentAdmin)
