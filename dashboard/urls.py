from django.urls import path

from dashboard.views import UpdatingTemplateView

app_name = 'dashboard'
urlpatterns = [
    path('', UpdatingTemplateView.as_view(), name='updating'),
]
