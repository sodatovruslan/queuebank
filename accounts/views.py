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
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if password1 != password2:
            return render(request, 'accounts/register.html', {'error': 'Password dont match'})
        elif User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'User already exist'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {'error': 'Email already exist'})
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_active = False
        user.save()
        Client.objects.create(user=user, full_name=username, phone='')
        send_confirmation_email(user)
        return render(request, 'accounts/confirm_email.html', {'username': user.username})
    return render(request, 'accounts/register.html')




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            not_active = User.objects.filter(username=username, is_active=False).first()
            if not_active:
                return render(request, 'accounts/login.html', {'error': 'Go and confirm your email'})
            else:
                return render(request, 'accounts/login.html', {'error': 'Wrong password or username'})
        else:
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')



def confirm_email(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        code = request.POST.get('code').strip()
        user = User.objects.filter(username=username).first()
        if not user:
            return render(request, 'accounts/confirm_email.html', {'error': 'Invalid username'})
        confirm = EmailConfirm.objects.filter(user=user, code=code).first()
        if not confirm:
            return render(request, 'accounts/confirm_email.html', {'error': 'Wrong code'})
        user.is_active = True
        user.save()
        confirm.delete()
        return redirect('login')
    return render(request, 'accounts/confirm_email.html')

# Create your views here.
