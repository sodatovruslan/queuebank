from django.db import models
from django.db import models
from django.contrib.auth.models import User
class Operator(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.full_name
# Create your models here.
