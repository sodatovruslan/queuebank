from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from tickets.models import Ticket, Window
from .models import Operator

@login_required
@permission_required('tickets.view_ticket', raise_exception=True)
def operator_panel(request):
    operator = Operator.objects.get(user=request.user)
    window = Window.objects.get(operator=operator)
    current_ticket = Ticket.objects.filter(
        window=window,
        status='called'
    ).first()
    
    queue = Ticket.objects.filter(
        service=window.service,
        status='waiting'
    )

    return render(request, 'operators/panel.html', {
        'window': window,
        'current_ticket': current_ticket,
        'queue': queue,
    })


@login_required
@permission_required('tickets.change_ticket', raise_exception=True)
def next_client(request):
    operator = Operator.objects.get(user=request.user)
    window = Window.objects.get(operator=operator)
    
    next_ticket = Ticket.objects.filter(
        service=window.service,
        status='waiting'
    ).first()
    
    if next_ticket:
        next_ticket.status = 'called'
        next_ticket.window = window
        next_ticket.save()

    return redirect('operator_panel')


@login_required
@permission_required('tickets.change_ticket', raise_exception=True)
def done_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.status = 'done'
    ticket.save()
    return redirect('operator_panel')


@login_required
@permission_required('tickets.change_ticket', raise_exception=True)
def skip_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.status = 'cancelled'
    ticket.save()
    return redirect('operator_panel')


@login_required
@permission_required('tickets.change_window', raise_exception=True)
def toggle_window(request):
    operator = Operator.objects.get(user=request.user)
    window = Window.objects.get(operator=operator)
    if window.is_open:
        window.is_open = False
    else:
        window.is_open = True
    window.save()
    return redirect('operator_panel')

# Create your views here.
