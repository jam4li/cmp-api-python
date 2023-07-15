from django.contrib import admin

from apps.base.admin import BaseAdmin

from .models import SupportTicket, SupportDepartment, SupportTicketReply

# Register your models here.


class SupportTicketReplyInline(admin.TabularInline):
    model = SupportTicketReply
    extra = 1


class SupportTicketAdmin(BaseAdmin):
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
        'content',
        'supportticketreply__content'
    ]

    fields = (
        'user',
        'department',
        'title',
        'content',
        'attachments',
        'important_level',
        'status',
        'admin_respondent',
        'is_admin_replied',
    ) + BaseAdmin.fields

    inlines = [
        SupportTicketReplyInline,
    ]

    list_display = [
        'user',
        'department',
        'title',
        'status',
        'is_admin_replied',
    ]

    readonly_fields = (
        'admin_respondent',
        'is_admin_replied',
    ) + BaseAdmin.fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('user')
        return qs

    def save_model(self, request, obj, form, change):
        if not obj.is_admin_replied:
            obj.is_admin_replied = True
        obj.admin_respondent = request.user  # Set the admin who replied
        super().save_model(request, obj, form, change)


admin.site.register(SupportTicket, SupportTicketAdmin)


class SupportDepartmentAdmin(BaseAdmin):
    search_fields = ['name']

    fields = (
        'name',
        'icon',
        'is_active',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields


admin.site.register(SupportDepartment, SupportDepartmentAdmin)
