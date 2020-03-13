from django.shortcuts import render
from rest_framework import generics, permissions
<<<<<<< HEAD:api/projects/views.py
from .models import (Project,
                    ProjectProfile, 
                    ProjectProfileImage, 
                    ProjectAnimal, 
                    ProjectPlant,
                    ProjectExpense,
                    ProjectEarning)
from .serializers import (ProjectsSerializer, 
                        ProjectProfileSerializer, 
                        ProfileImageSerializer,
                        ProjectExpenseSerializer,
                        ProjectEarningSerializer)
from rest_framework_jwt.settings import api_settings
from .decorators import (validated_data, 
                        validate_profile_data, 
                        validate_image_data, 
                        validate_animal_data, 
                        validate_plant_data,
                        validate_expenses_data,
                        validate_earnings_data)
=======
from api.apps.projects.models import Project, ProjectProfile, ProjectProfileImage, ProjectAnimal, ProjectPlant
from api.apps.projects.serializers import ProjectsSerializer, ProjectProfileSerializer, ProfileImageSerializer
from rest_framework_jwt.settings import api_settings
from api.apps.projects.decorators import validated_data, validate_profile_data, validate_image_data, validate_animal_data, validate_plant_data
>>>>>>> Extending the user model:api/apps/projects/views.py
from rest_framework.response import Response
from rest_framework import status
from api.apps.animals.models import Animal
from api.apps.plants.models import Plant

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = (permissions.IsAuthenticated, )
  
    """
    NB. at a point of creating a project, is when the animals and plants are added
    structure for plants 
    {
        "animals":[
        {
            'animal_id':'1',
            'project_id':'1',
            'no':50
        },
        ],
        "plants":[
        {
            'plant_id':'1',
            'project_id':'1',
            'no':50
        },
        ]
    }
    """
    @validated_data
    def post(self, request, *args, **kwargs):

        data={
            'alias': request.data.get('alias', ''),
            'description': request.data.get('description', ''),
            'start_date': request.data.get('start_date', ''),
            'harvest_start_date': request.data.get('harvest_start_date', ''),
            'estimated_harvest_duration': request.data.get(
                'estimated_harvest_duration', ''),
            'actual_harvest_end_date': request.data.get(
                'actual_harvest_end_date', ''),
            'plants':request.data.get('animals', []),
            'animals': request.data.get('plants', [])
        }
        
        project = ProjectsSerializer(data=data)
        project.is_valid(raise_exception=True)
        project.save()
        return Response(status=status.HTTP_201_CREATED)


class ProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(pk=kwargs['pk'])
            serializer = ProjectsSerializer(project)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(data={
                'massage': 'project with id {} was not found'.format(kwargs['pk'])
            })

    @validated_data
    def put(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(pk=kwargs['pk'])
            serializer = ProjectsSerializer()
            update_project = serializer.update(project, request.data)
            return Response(status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(data={
                'massage': 'project with id {} was not found'.format(kwargs['pk'])
            })

    def delete(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(pk=kwargs['pk'])
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Project.DoesNotExist:
            return Response(data={
                'massage': 'project with id {} was not found'.format(kwargs['pk'])
            })

class ProjectExpensesListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProjectExpense.objects.all()
    serializer_class = ProjectExpenseSerializer

    """
    get all expenses for a given project
    GET expenses/:id <- project id
    POST expenses/:id <- project id
    """

    def get(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(pk=kwargs['pk'])
            expenses = ProjectExpense.objects.filter(project_id=project)
            data = ProjectExpenseSerializer(expenses, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(
                data={
                    "massage": 'project with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @validate_expenses_data
    def post(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(pk=kwargs['pk'])
            ProjectExpense.objects.create(
                project_id = project,
                exp_type = request.data.get('exp_type', ''),
                amount= request.data.get('amount', ''),
                comment= request.data.get('comment', ''),
                date_spent = request.data.get('date_spent', '')
            )
            return Response(status=status.HTTP_201_CREATED)

        except Project.DoesNotExist:
            return Response(
                data={
                    "massage": 'project with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProjectExpensesDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    get a particular profile i.e with its images
    update profile info
    delete profile
    NB. main difference is the (s) on the url
    GET expense/:id
    PUT expense/:id
    DELETE expense/:id
    """
    queryset = ProjectExpense.objects.all()
    serializer_class = ProjectExpenseSerializer

    def get(self, request, *args, **kwargs):
        try:
            expense = ProjectExpense.objects.get(pk=kwargs['pk'])
            return Response(data=ProjectExpenseSerializer(expense).data, status=status.HTTP_200_OK)
        except ProjectExpense.DoesNotExist:
            return Response(data={
                "message": 'project expense with id {} does not exist'.format(kwargs['pk'])
            })

    @validate_expenses_data 
    def put(self, request, *args, **kwargs):
        try:
            expense = ProjectExpense.objects.get(pk=kwargs['pk'])
            serializer = ProjectExpenseSerializer()
            serializer.update(expense, request.data)
            return Response(status=status.HTTP_200_OK)
        except ProjectExpense.DoesNotExist:
            return Response(data={
                "message": 'project expense with id {} does not exist'.format(kwargs['pk'])
            })

    def delete(self, request, *args, **kwargs):
        try:
            expense = ProjectExpense.objects.get(pk=kwargs['pk'])
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProjectExpense.DoesNotExist:
            return Response(data={
                "message": 'project expense with id {} does not exist'.format(kwargs['pk'])
            })


class ProjectEarningsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProjectEarning.objects.all()
    serializer_class = ProjectEarningSerializer

    """
    get all earnings for a given project
    GET earnings/:id <- project id
    POST earnings/:id <- project id
    """

    def get(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(pk=kwargs['pk'])
            earnings = ProjectEarning.objects.filter(project_id=project)
            data = ProjectEarningSerializer(earnings, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(
                data={
                    "massage": 'project with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @validate_earnings_data
    def post(self, request, *args, **kwargs):
        
        try:
            project = Project.objects.get(pk=kwargs['pk'])
            ProjectEarning.objects.create(
                project_id = project,
                amount_earned= request.data.get('amount_earned', ''),
                date_earned = request.data.get('date_earned', '')
            )
            return Response(status=status.HTTP_201_CREATED)

        except Project.DoesNotExist:
            return Response(
                data={
                    "massage": 'project with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProjectEarningsDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    get a particular earning
    NB. main difference is the (s) on the url
    GET earning/:id
    PUT earning/:id
    DELETE earning/:id
    """
    queryset = ProjectEarning.objects.all()
    serializer_class = ProjectEarningSerializer

    def get(self, request, *args, **kwargs):
        try:
            earning = ProjectEarning.objects.get(pk=kwargs['pk'])
            return Response(data=ProjectEarningSerializer(earning).data, status=status.HTTP_200_OK)
        except ProjectEarning.DoesNotExist:
            return Response(data={
                "message": 'project earning with id {} does not exist'.format(kwargs['pk'])
            })

    @validate_earnings_data
    def put(self, request, *args, **kwargs):
        try:
            earning = ProjectEarning.objects.get(pk=kwargs['pk'])
            serializer = ProjectEarningSerializer()
            serializer.update(earning, request.data)
            return Response(status=status.HTTP_200_OK)
        except ProjectEarning.DoesNotExist:
            return Response(data={
                "message": 'project earning with id {} does not exist'.format(kwargs['pk'])
            })

    def delete(self, request, *args, **kwargs):
        try:
            earning = ProjectEarning.objects.get(pk=kwargs['pk'])
            earning.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProjectEarning.DoesNotExist:
            return Response(data={
                "message": 'project earning with id {} does not exist'.format(kwargs['pk'])
            })


class ProjectPlantCreateAPIView(generics.CreateAPIView):
    """
    can be used to add plant to project
    POST profile_image/:id <-- profile_id
    """
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer

    @validate_plant_data
    def post(self, request, *args, **kwargs):
        plant_id = request.data.get('plant_id', '')
        no = request.data.get('no', '')

        try:
            project = Project.objects.get(pk=kwargs['pk'])
            plant = Plant.objects.get(pk=plant_id)
            ProjectPlant.objects.create(
                plant_id=plant,
                project_id=project,
                no=no
            )
            return Response(status=status.HTTP_201_CREATED)

        except Project.DoesNotExist:
            return Response(
                data={
                    "massage": 'profile with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProjectPlantDestroyView(generics.DestroyAPIView):
    """
    can be used to add image to profile
    DELETE profile_image/:id <-- image_id
    """
    queryset = ProjectPlant.objects.all()
    serializer_class = ProjectsSerializer

    def delete(self, request, *args, **kwargs):

        try:
            project_plant = ProjectPlant.objects.get(pk=kwargs['pk'])
            project_plant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProjectPlant.DoesNotExist:
            return Response(
                data={
                    "massage": 'project plant with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class ProjectAnimalCreateAPIView(generics.CreateAPIView):
    """
    can be used to add an animal to a project
    POST project_animal/:id <-- project_id
    """
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer

    @validate_animal_data
    def post(self, request, *args, **kwargs):
        animal_id = request.data.get('animal_id', '')
        no = request.data.get('no', '')

        try:
            project = Project.objects.get(pk=kwargs['pk'])
            animal = Animal.objects.get(pk=animal_id)

            ProjectAnimal.objects.create(
                project_id=project,
                animal_id=animal,
                no=no
            )
            return Response(status=status.HTTP_201_CREATED)

        except Project.DoesNotExist:
            return Response(
                data={
                    "massage": 'profile with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProjectAnimalDestroyView(generics.DestroyAPIView):
    """
    can be used to add image to profile
    DELETE profile_image/:id <-- image_id
    """
    queryset = ProjectAnimal.objects.all()
    serializer_class = ProjectsSerializer

    def delete(self, request, *args, **kwargs):

        try:
            project_animal = ProjectAnimal.objects.get(pk=kwargs['pk'])
            project_animal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProjectAnimal.DoesNotExist:
            return Response(
                data={
                    "massage": 'profile with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProjectProfileListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProjectProfile.objects.all()
    serializer_class = ProjectProfileSerializer

    """
    NB. at a point of creating a profile, is when the profile images are added
    structure for images 
    [
        {
            'url':'jajj.png',
            'caption':''
        },
        {
            'url':'jajj.png',
            'caption':''
        },
    ]
    get all profiles for a given project
    GET profiles/:id <- project id
    POST profiles/:id <- project id
    """

    def get(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(pk=kwargs['pk'])
            profiles = ProjectProfile.objects.filter(project_id=project)
            data = ProjectProfileSerializer(profiles, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(
                data={
                    "massage": 'project with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @validate_profile_data
    def post(self, request, *args, **kwargs):
        data = {
            'project_id': kwargs['pk'],
            'project_stage': request.data.get('project_stage', ''),
            'stage_caption': request.data.get('stage_caption', ''),
            'detailed_explanation': request.data.get('detailed_explanation', ''),
            'images': request.data.get('images', [])
        }

        try:
            project = Project.objects.get(pk=kwargs['pk'])
            serializer = ProjectProfileSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        except Project.DoesNotExist:
            return Response(
                data={
                    "massage": 'project with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProjectProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    get a particular profile i.e with its images
    update profile info
    delete profile
    NB. main difference is the (s) on the url
    GET profile/:id
    PUT profile/:id
    DELETE profile/:id
    """
    queryset = ProjectProfile.objects.all()
    serializer_class = ProjectProfileSerializer

    def get(self, request, *args, **kwargs):
        try:
            profile = ProjectProfile.objects.get(pk=kwargs['pk'])
            return Response(data=ProjectProfileSerializer(profile).data, status=status.HTTP_200_OK)
        except ProjectProfile.DoesNotExist:
            return Response(data={
                "message": 'project profile with id {} does not exist'.format(kwargs['pk'])
            })

    @validate_profile_data
    def put(self, request, *args, **kwargs):
        try:
            profile = ProjectProfile.objects.get(pk=kwargs['pk'])
            serializer = ProjectProfileSerializer()
            serializer.update(profile, request.data)
            return Response(status=status.HTTP_200_OK)
        except ProjectProfile.DoesNotExist:
            return Response(data={
                "message": 'project profile with id {} does not exist'.format(kwargs['pk'])
            })

    def delete(self, request, *args, **kwargs):
        try:
            profile = ProjectProfile.objects.get(pk=kwargs['pk'])
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProjectProfile.DoesNotExist:
            return Response(data={
                "message": 'project profile with id {} does not exist'.format(kwargs['pk'])
            })


class ProfileImagesCreateAPIView(generics.CreateAPIView):
    """
    can be used to add image to profile
    POST profile_image/:id <-- profile_id
    """
    queryset = ProjectProfile.objects.all()
    serializer_class = ProfileImageSerializer

    @validate_image_data
    def post(self, request, *args, **kwargs):
        image_url = request.data.get('image_url', '')
        image_caption = request.data.get('image_caption', '')

        try:
            profile = ProjectProfile.objects.get(pk=kwargs['pk'])
            serializer = ProjectProfileSerializer()
            ProjectProfileImage.objects.create(
                profile_id=profile,
                image_url=image_url,
                image_caption=image_caption
            )
            return Response(status=status.HTTP_201_CREATED)

        except ProjectProfile.DoesNotExist:
            return Response(
                data={
                    "massage": 'profile with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileImagesDestroyView(generics.DestroyAPIView):
    """
    can be used to add image to profile
    DELETE profile_image/:id <-- image_id
    """
    queryset = ProjectProfileImage.objects.all()
    serializer_class = ProfileImageSerializer

    def delete(self, request, *args, **kwargs):

        try:
            profile_image = ProjectProfileImage.objects.get(pk=kwargs['pk'])
            profile_image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProjectProfileImage.DoesNotExist:
            return Response(
                data={
                    "massage": 'profile with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )
