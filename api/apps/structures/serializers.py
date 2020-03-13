
from rest_framework import serializers
from api.apps.structures.models import Structure

class StructuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = ('alias','purpose','capacity', 'dimensions', 'setup_cost')
