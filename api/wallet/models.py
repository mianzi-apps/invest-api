from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Wallet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bal = models.DecimalField(max_digits=40, decimal_places=30,default=0.0)
