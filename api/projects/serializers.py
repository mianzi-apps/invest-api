from rest_framework import serializers
from .models import Project, ProjectAnimal, ProjectPlant, ProjectEarnings, ProjectExpenses, ProjectProfile, ProjectProfileImages

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('alias', 'description', 'start_date', 'harvest_start_date', 
                'estimated_harvest_duration', 'actual_harvest_end_date')