from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service, Ticket, Window

def home(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'tickets/home.html', {'services': services})
# Create your views here.
