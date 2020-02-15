from django.db import models
from api.apps.authentication.models import User


# Create your models here.
class Wallet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=40, decimal_places=30,default=0.0)
