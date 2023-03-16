from django.contrib import admin

from .models import Ticket, TicketDepartment, TicketReply

# Register your models here.


class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 1


class TicketAdmin(admin.ModelAdmin):
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
        TicketReplyInline,
    ]


admin.site.register(Ticket, TicketAdmin)


class TicketDepartmentAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'icon',
        'is_active',
    )


admin.site.register(TicketDepartment, TicketDepartmentAdmin)
