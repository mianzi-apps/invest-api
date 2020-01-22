from rest_framework import serializers
from .models import Farm, Location

class FarmsSelializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ('name', 'location', 'start_date')
    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('district', 'city', 'latitude', 'longitude')