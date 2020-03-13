
from rest_framework import serializers
from .models import Structure

class StructuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = ('alias','purpose','capacity', 'dimensions', 'setup_cost')
