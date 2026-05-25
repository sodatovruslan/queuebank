from django.db import models
from django.contrib.auth.models import User
from operators.models import Operator
class Service(models.Model):
    name=models.CharField(max_length=100)
    code=models.CharField(max_length=5)
    description=models.TextField(blank=True, null=True)
    is_active=models.BooleanField(default=True)



    def __str__(self):
        return f"{self.code} - {self.name}"


class Window(models.Model):
    number=models.IntegerField()
    is_open=models.BooleanField(default=True)
    operator=models.OneToOneField(Operator, on_delete=models.CASCADE)
    service= models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"Окно №{self.number}"


class Ticket(models.Model):

    STATUS = [
        ('waiting',   'Ожидает'),
        ('called',    'Вызван'),
        ('done',      'Обслужен'),
        ('cancelled', 'Отменён'),
    ]

    number=models.CharField(max_length=10)
    status=models.CharField(max_length=20, choices=STATUS, default='waiting')
    created_at=models.DateTimeField(auto_now_add=True)
    called_at=models.DateTimeField(null=True, blank=True)
    served_at=models.DateTimeField(null=True, blank=True)
    client=models.ForeignKey(User, on_delete=models.CASCADE)
    service=models.ForeignKey(Service, on_delete=models.CASCADE)
    window=models.ForeignKey(Window, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.number} - {self.status}"

# Create your models here.
