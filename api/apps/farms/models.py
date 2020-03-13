from django.db import models


class Location(models.Model):
    district = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    latitude = models.CharField(max_length=255, null=True, )
    longitude = models.CharField(max_length=255, null=True, )


class Farm(models.Model):
    name = models.CharField(max_length=255, null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
