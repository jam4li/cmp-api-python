from django.urls import path

from apps.support.views.user_views import SupportDepartmentListAPIView, SupportTicketCreateAPIView, SupportTicketListAPIView, SupportTicketDetailAPIView

app_name = 'support_user'

urlpatterns = [
    path(
        'department/list/',
        SupportDepartmentListAPIView.as_view(),
        name='department-list',
    ),
    path(
        'ticket/create/',
        SupportTicketCreateAPIView.as_view(),
        name='ticket-create',
    ),
    path(
        'ticket/list/',
        SupportTicketListAPIView.as_view(),
        name='ticket-list',
    ),
    path(
        'ticket/detail/<int:pk>/',
        SupportTicketDetailAPIView.as_view(),
        name='ticket-detail',
    )
]
