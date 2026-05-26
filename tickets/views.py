from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service, Ticket, Window

def home(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'tickets/home.html', {'services': services})


@login_required
def take_ticket(request, pk):
    service = Service.objects.get(pk=pk)
    count = Ticket.objects.filter(service=service).count()
    number = f"{service.code}{count + 1:03d}"
    Ticket.objects.create(
        number=number,
        client=request.user,
        service=service,
        status='waiting'
    )
    return redirect('my_ticket')
# Create your views here.
