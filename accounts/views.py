from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Client

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        Client.objects.create(user=user, full_name=username, phone='')
        return redirect('login')
    return render(request, 'accounts/register.html')

# Create your views here.
