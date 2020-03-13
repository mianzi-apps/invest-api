from rest_framework import serializers
from .models import (Project,
                    ProjectAnimal, 
                    ProjectPlant, 
                    ProjectEarning, 
                    ProjectExpense, 
                    ProjectProfile,
                    ProjectProfileImage)

from animals.serializers import AnimalSerializer
from plants.serializers import PlantSerializer

class ProjectAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAnimal
        fields = ('animal_id', 'no')

class ProjectPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlant
        fields = ('plant_id', 'no')


class ProjectsSerializer(serializers.ModelSerializer):
    animals = ProjectAnimalSerializer(many=True)
    plants = ProjectPlantSerializer(many=True)
    
    class Meta:
        model = Project
        fields = ('alias', 'description', 'start_date', 'harvest_start_date', 
                'estimated_harvest_duration', 'actual_harvest_end_date', 'animals', 'plants')

    def create(self, validated_data): 
        animals_data = validated_data.pop('animals')
        plants_data = validated_data.pop('plants')
        
        project = Project.objects.create(**validated_data)
        
        for animal in animals_data:
            ProjectAnimal.objects.create(project_id=project, **animal)
        
        for plant in plants_data:
            ProjectPlant.objects.create(project_id=project, **plant)
        
        return project

        

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectProfileImage
        fields = ('image_url', 'image_caption')


class ProjectProfileSerializer(serializers.ModelSerializer):
    images = ProfileImageSerializer(many=True)
    class Meta:
        model = ProjectProfile
        fields = ('project_id', 'project_stage' ,'stage_caption' , 'detailed_explanation', 'images')
        
    def create(self, validated_data):
        images_data = validated_data.pop('images')
        profile = ProjectProfile.objects.create(**validated_data)

        for image in images_data:
            ProjectProfileImage.objects.create(profile_id=profile, **image)
        return profile


class ProjectExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectExpense
        fields = ('exp_type', 'amount', 'comment', 'date_spent')


class ProjectEarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEarning
        fields = ('amount_earned', 'date_earned')