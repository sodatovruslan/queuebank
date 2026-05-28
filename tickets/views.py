from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from .models import Service, Ticket, Window


from groq import Groq

GROQ_API_KEY = ''

def ai_help(request):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = request.GET.get('prompt', '').strip()
    
    services = Service.objects.filter(is_active=True)
    
    services_for_ai = []
    for service in services:
        services_for_ai.append({
            'name': service.name,
            'code': service.code,
            'description': service.description,
        })
    
    PROMPT_FOR_AI = f"""
    You are a helpful assistant for QueueBank.
    Our bank has these services: {services_for_ai}
    Help clients choose the right service and answer questions about the queue system.
    Answer in the same language the user writes in.
    """
    
    answer = ''
    if prompt:
        response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": PROMPT_FOR_AI},
        {"role": "user", "content": prompt}
    ],
    model="llama-3.3-70b-versatile",
)
        
        answer = response.choices[0].message.content
    
    return render(request, 'tickets/ai_help.html', {
        'answer': answer,
        'prompt': prompt,
        'services': services,
    })


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


@login_required
@permission_required('tickets.change_ticket', raise_exception=True)
def cancel_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if ticket.client == request.user:
        ticket.status = 'cancelled'
        ticket.save()
    return redirect('my_ticket')



@login_required
@permission_required('tickets.view_ticket', raise_exception=True)
def ticket_history(request):
    tickets = Ticket.objects.filter(
        client=request.user
    ).order_by('-created_at')
    return render(request, 'tickets/history.html', {'tickets': tickets})
# Create your views here.
