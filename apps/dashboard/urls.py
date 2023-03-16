from django.urls import path

from .views import UpdatingTemplateView

app_name = 'dashboard'
urlpatterns = [
    path('', UpdatingTemplateView.as_view(), name='updating'),
]
