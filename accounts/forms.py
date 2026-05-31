from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )
    
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    
class ConfirmEmailForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your code'})
    )
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

class ResetConfirmForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your code'}))
    new_password = forms.CharField(
    widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))