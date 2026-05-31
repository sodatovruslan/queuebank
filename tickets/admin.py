from django.contrib import admin
from .models import Service, Window, Ticket,Message

admin.site.register(Service)
admin.site.register(Window)
admin.site.register(Ticket)
admin.site.register(Message)
# Register your models here.
