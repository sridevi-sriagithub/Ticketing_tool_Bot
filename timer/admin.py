from django.contrib import admin
from .models import Ticket,SLATimer

# Register your models here.
admin.site.register(Ticket)
admin.site.register(SLATimer)
# admin.site.register(SLATimeHistory)
