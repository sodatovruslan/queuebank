from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from .models import Service, Ticket, Window

def home(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'tickets/home.html', {'services': services})


@login_required
@permission_required('tickets.add_ticket', raise_exception=True)
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


@login_required
@permission_required('tickets.view_ticket', raise_exception=True)
def my_ticket(request):
    ticket = Ticket.objects.filter(
        client=request.user
    ).last()

    position = Ticket.objects.filter(
        service=ticket.service,
        status='waiting'
    ).count()

    return render(request, 'tickets/my_ticket.html', {
        'ticket': ticket,
        'position': position
    })
# Create your views here.
