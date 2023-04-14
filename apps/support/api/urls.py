from django.urls import path

from .views import SupportDepartmentListAPIView, SupportTicketCreateAPIView, SupportTicketListAPIView

app_name = 'support'
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
