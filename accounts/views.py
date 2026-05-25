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


from django.contrib.auth import login, logout, authenticate

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

# Create your views here.
