from django.urls import path
from . import views

urlpatterns = [
    path('panel/', views.operator_panel, name='operator_panel'),
    path('next/', views.next_client, name='next_client'),
    path('done/<int:ticket_id>/', views.done_ticket, name='done_ticket'),
    path('skip/<int:ticket_id>/', views.skip_ticket, name='skip_ticket'),
]