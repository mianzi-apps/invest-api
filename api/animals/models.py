from django.db import models

class Animal(models.Model):
    english_name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    # maturity period in days
    estimated_maturity_period = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)