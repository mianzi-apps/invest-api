from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Project, ProjectProfile, ProjectProfileImage
from .serializers import ProjectsSerializer, ProjectProfileSerializer, ProfileImageSerializer
from rest_framework_jwt.settings import api_settings
from .decorators import validated_data, validate_profile_data, validate_image_data
from rest_framework.response import Response
from rest_framework import status

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @validated_data
    def post(self, request, *args, **kwargs):
        alias = request.data.get('alias', '')
        description = request.data.get('description', '')
        start_date = request.data.get('start_date', '')
        harvest_start_date = request.data.get('harvest_start_date', '')
        estimated_harvest_duration = request.data.get('estimated_harvest_duration', '')
        actual_harvest_end_date = request.data.get('actual_harvest_end_date', '')

        Project.objects.create(
            alias=alias, 
            description=description, 
            start_date=start_date,
            harvest_start_date=harvest_start_date, 
            estimated_harvest_duration=estimated_harvest_duration, 
            actual_harvest_end_date=actual_harvest_end_date
        )
        return Response(status=status.HTTP_201_CREATED)

class ProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(pk=kwargs['pk'])
            return Response(data=ProjectsSerializer(project).data, status=status.HTTP_200_OK)
        
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
            return Response(data=ProjectsSerializer(project).data, status=status.HTTP_200_OK)
        
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


class ProjectProfileListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProjectProfile.objects.all()
    serializer_class = ProjectProfileSerializer
    
    """
    NB. at a point of creating a project, is when the profile images are added
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
                    "massage" :'project with id {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @validate_profile_data
    def post(self, request, *args, **kwargs):
        data = {
            'project_id': kwargs['pk'],
            'project_stage': request.data.get('project_stage',''),
            'stage_caption': request.data.get('stage_caption',''),
            'detailed_explanation': request.data.get('detailed_explanation',''),
            'images': request.data.get('images',[])
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
                    "massage" :'project with id {} does not exist'.format(kwargs['pk'])
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
        image_url = request.data.get('image_url','')
        image_caption = request.data.get('image_caption','')
        
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
                    "massage" :'profile with id {} does not exist'.format(kwargs['pk'])
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
                        "massage" :'profile with id {} does not exist'.format(kwargs['pk'])
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )


class ProjectExpenseCreateAPIView(generics.ListCreateAPIView):
    pass


class ProjectExpenseDetails(generics.RetrieveUpdateDestroyAPIView):
    pass


class ProjectEarningCreateAPIView(generics.ListCreateAPIView):
    pass


class ProjectEarningDetails(generics.RetrieveUpdateDestroyAPIView):
    pass


class ProjectPlantCreateAPIView(generics.ListCreateAPIView):
    pass


class ProjectPlantDetails(generics.RetrieveUpdateDestroyAPIView):
    pass


class ProjectAnimalCreateAPIView(generics.ListCreateAPIView):
    pass


class ProjectAnimalDetails(generics.RetrieveUpdateDestroyAPIView):
    pass
