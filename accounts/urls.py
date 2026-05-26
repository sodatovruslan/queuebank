from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('confirm-email/', views.confirm_email, name='confirm_email'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-confirm/', views.reset_confirm, name='reset_confirm'),
]