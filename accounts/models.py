from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)

    def __str__(self):
        return self.full_name
    

class EmailConfirm(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	code=models.CharField(max_length=6)


	def __str__(self):
		return self.user.username
# Create your models here.
