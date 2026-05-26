from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('take/<int:pk>/', views.take_ticket, name='take_ticket'),
    path('my-ticket/', views.my_ticket, name='my_ticket'),
]