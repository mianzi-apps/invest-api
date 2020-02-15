from rest_framework import serializers
from api.apps.animals.models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ('english_name', 'scientific_name', 'estimated_maturity_period')