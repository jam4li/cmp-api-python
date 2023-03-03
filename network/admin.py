from django.contrib import admin

from .models import Network, NetworkTreeTransfer, NetworkTreeTransferred

# Register your models here.


admin.site.register(Network)


admin.site.register(NetworkTreeTransfer)


admin.site.register(NetworkTreeTransferred)
