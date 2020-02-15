from rest_framework import serializers
from api.apps.plants.models import Plant

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ('english_name', 'scientific_name', 'estimated_maturity_period')
