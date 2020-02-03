from rest_framework import serializers
from .models import Project, ProjectAnimal, ProjectPlant, ProjectEarning, ProjectExpense, ProjectProfile, ProjectProfileImage

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('alias', 'description', 'start_date', 'harvest_start_date', 
                'estimated_harvest_duration', 'actual_harvest_end_date')


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

    # def to_representation(self, value):
    #     """
    #     Serialize ProjectProfileImage instances using a ProjectProfileImage serializer
    #     """
    #     if isinstance(value, ProjectProfileImage):
    #         serializer = ProfileImageSerializer(value)
    #     else:
    #         raise Exception('Unexpected type of tagged object')
    #     return serializer.data