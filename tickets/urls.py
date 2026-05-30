from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('take/<int:pk>/', views.take_ticket, name='take_ticket'),
    path('my-ticket/', views.my_ticket, name='my_ticket'),
    path('cancel/<int:pk>/', views.cancel_ticket, name='cancel_ticket'),
    path('history/', views.ticket_history, name='ticket_history'),
    path('ai-help/', views.ai_help, name='ai_help'),
	path('chat/<int:pk>/', views.chat, name='chat'),
]