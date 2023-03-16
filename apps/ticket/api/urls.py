from django.urls import path

from .views import TicketDepartmentListAPIView

app_name = 'ticket'
urlpatterns = [
    path('department/list/', TicketDepartmentListAPIView.as_view()),
]
