from django.urls import path

from home.views import UpdatingTemplateView

app_name = 'home'
urlpatterns = [
    path('', UpdatingTemplateView.as_view(), name='updating'),
]
