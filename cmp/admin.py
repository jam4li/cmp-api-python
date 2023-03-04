from django.contrib import admin

from .models import CMPToken, CMPClaimHistory, CMPTokenTransaction

# Register your models here.


admin.site.register(CMPToken)

admin.site.register(CMPClaimHistory)

admin.site.register(CMPTokenTransaction)
