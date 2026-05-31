from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from tickets.models import Ticket, Service, Window
from operators.models import Operator
from .forms import CreateOperatorForm

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


@login_required
def create_operator(request):
    if not request.user.is_superuser:
        return redirect('home')
    form = CreateOperatorForm()
    if request.method == 'POST':
        form = CreateOperatorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            full_name = form.cleaned_data['full_name']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                password=password
            )
            user.is_staff = True
            user.save()
            group = Group.objects.get(name='operator')
            user.groups.add(group)
            Operator.objects.create(user=user, full_name=full_name)
            return redirect('dashboard')
    return render(request, 'dashboard/create_operator.html', {'form': form})
# Create your views here.
