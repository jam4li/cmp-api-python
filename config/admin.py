from django.contrib import admin

from .models import Config, DailyProfit

# Register your models here.


admin.site.register(Config)

admin.site.register(DailyProfit)
