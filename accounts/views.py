from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from random import randint
from django.core.mail import send_mail
from .models import EmailConfirm, Client
from django.conf import settings
from .forms import RegisterForm, LoginForm, ConfirmEmailForm, ForgotPasswordForm, ResetConfirmForm
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
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 != password2:
                return render(request, 'accounts/register.html', {'form': form, 'error': 'Password dont match'})
            elif User.objects.filter(username=username, is_active=True).exists():
                return render(request, 'accounts/register.html', {'form': form, 'error': 'User already exist'})
            elif User.objects.filter(email=email, is_active=True).exists():
                return render(request, 'accounts/register.html', {'form': form, 'error': 'Email already exist'})
            User.objects.filter(username=username, is_active=False).delete()
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.is_active = False
            user.save()
            Client.objects.create(user=user, full_name=username, phone='')
            send_confirmation_email(user)
            return render(request, 'accounts/confirm_email.html', {'username': user.username})
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if not user:
                not_active = User.objects.filter(username=username, is_active=False).first()
                if not_active:
                    return render(request, 'accounts/login.html', {'form': form, 'error': 'Go and confirm your email'})
                else:
                    return render(request, 'accounts/login.html', {'form': form, 'error': 'Wrong password or username'})
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def confirm_email(request):
    form = ConfirmEmailForm()
    if request.method == 'POST':
        form = ConfirmEmailForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username').strip()
            code = form.cleaned_data['code'].strip()
            user = User.objects.filter(username=username).first()
            if not user:
                return render(request, 'accounts/confirm_email.html', {'form': form, 'error': 'Invalid username'})
            confirm = EmailConfirm.objects.filter(user=user, code=code).first()
            if not confirm:
                return render(request, 'accounts/confirm_email.html', {'form': form, 'error': 'Wrong code'})
            user.is_active = True
            user.save()
            confirm.delete()
            return redirect('login')
    return render(request, 'accounts/confirm_email.html', {'form': form})


def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip()
            user = User.objects.filter(email=email).first()
            if not user:
                return render(request, 'accounts/forgot_password.html', {'form': form, 'error': 'Email not found'})
            send_confirmation_email(user)
            return redirect('reset_confirm')
    return render(request, 'accounts/forgot_password.html', {'form': form})


def reset_confirm(request):
    form = ResetConfirmForm()
    if request.method == 'POST':
        form = ResetConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip()
            new_password = form.cleaned_data['new_password']
            confirm = EmailConfirm.objects.filter(code=code).first()
            if not confirm:
                return render(request, 'accounts/reset_confirm.html', {'form': form, 'error': 'Wrong code'})
            user = confirm.user
            user.set_password(new_password)
            user.save()
            confirm.delete()
            return redirect('login')
    return render(request, 'accounts/reset_confirm.html', {'form': form})