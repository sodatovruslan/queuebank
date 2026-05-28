from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from tickets.models import Ticket, Service, Window

@login_required
@permission_required('tickets.view_ticket', raise_exception=True)
def dashboard(request):
    total_today = Ticket.objects.filter(status='done').count()
    waiting = Ticket.objects.filter(status='waiting').count()
    called = Ticket.objects.filter(status='called').count()
    cancelled = Ticket.objects.filter(status='cancelled').count()
    open_windows = Window.objects.filter(is_open=True).count()
    services = Service.objects.filter(is_active=True)

    return render(request, 'dashboard/dashboard.html', {
        'total_today': total_today,
        'waiting': waiting,
        'called': called,
        'cancelled': cancelled,
        'open_windows': open_windows,
        'services': services,
    })
# Create your views here.
