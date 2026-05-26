from django.contrib import admin
from .models import Client, EmailConfirm

admin.site.register(Client)
admin.site.register(EmailConfirm)
# Register your models here.
