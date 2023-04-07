from django.urls import path

from .views import SupportDepartmentListAPIView

app_name = 'support'
urlpatterns = [
    path('department/list/', SupportDepartmentListAPIView.as_view()),
]
