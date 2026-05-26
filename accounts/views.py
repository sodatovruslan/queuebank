from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from random import randint
from django.core.mail import send_mail
from .models import EmailConfirm, Client
from django.conf import settings

def send_confirmation_email(user):
    code = randint(100000, 999999)
    EmailConfirm.objects.update_or_create(user=user, defaults={'code': code})
    try:
        send_mail(
            subject='Confirm ur Password',
            message=f'Hello {user.username}, your code is {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email])
    except Exception as e:
        print(e, 'error')

def register(request):
    if request.method=="POST":
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
