from django import views
from django.shortcuts import render

# Create your views here.


class UpdatingTemplateView(views.View):
    def get(self, request, pk=None, *args, **kwargs):
        return render(request, 'updaing.html', {})
