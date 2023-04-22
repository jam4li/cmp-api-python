from django.urls import path

from apps.support.views.user_views import SupportDepartmentListAPIView, SupportTicketCreateAPIView, SupportTicketListAPIView

app_name = 'support_user'

urlpatterns = [
    path(
        'department/list/',
        SupportDepartmentListAPIView.as_view(),
    ),
    path(
        'ticket/create/',
        SupportTicketCreateAPIView.as_view(),
    ),
    path(
        'ticket/list/',
        SupportTicketListAPIView.as_view(),
    ),
]
