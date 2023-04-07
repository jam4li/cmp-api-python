from django.contrib import admin

from .models import SupportTicket, SupportDepartment, SupportTicketReply

# Register your models here.


class SupportTicketReplyInline(admin.TabularInline):
    model = SupportTicketReply
    extra = 1


class SupportTicketAdmin(admin.ModelAdmin):
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


admin.site.register(SupportTicket, SupportTicketAdmin)


class SupportDepartmentAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'icon',
        'is_active',
    )


admin.site.register(SupportDepartment, SupportDepartmentAdmin)
