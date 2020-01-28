from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Project
from .serializers import ProjectsSerializer
from rest_framework_jwt.settings import api_settings
from .decorators import validated_data
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



class ProjectProfileCreateAPIView(generics.ListCreateAPIView):
    pass


class ProjectProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    pass

class ProfileImagesCreateAPIView(generics.ListCreateAPIView):
    pass


class ProfileImagesDetails(generics.RetrieveUpdateDestroyAPIView):
    pass


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
