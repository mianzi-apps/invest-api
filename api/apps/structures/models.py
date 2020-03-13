from django.db import models
from api.apps.farms.models import Farm


class Structure(models.Model):
    alias=models.CharField(max_length=255)
    purpose=models.TextField(max_length=300)
    capacity=models.IntegerField()
    dimensions=models.CharField(max_length=150)
    setup_cost=models.IntegerField()
    farm_id=models.ForeignKey(Farm,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)