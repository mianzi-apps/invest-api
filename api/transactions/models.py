from django.db import models


class Transaction(models.Model):
    TYPES = (
        ('D' ,'deposit'),
        ('W','withdraw')
    )
    STATUSES = (
        ('P','pending'),
        ('C','complete'),
        ('C','canceled')
    )
    amount = models.DecimalField(max_digits=40, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=1, choices=TYPES)
    status = models.CharField(max_length=1, choices=STATUSES)
