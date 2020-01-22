from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import Response, status
from .models import Farm, Location
from .selializers import FarmsSelializer, LocationSerializer
from rest_framework_jwt.settings import api_settings
from .decorators import validate_request_data

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.
class ListCreateFarmsView(generics.ListCreateAPIView):
    """
    GET farms/
    POST farms/
    """
    queryset = Farm.objects.all()
    serializer_class = FarmsSelializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request, *args, **kwargs):
        name = request.data.get('name', '')
        location_id = request.data.get('location', '')
        start_date = request.data.get('start_date', '')

        Farm.objects.create(name=name, 
                                    location=Location.objects.get(pk=location_id), 
                                    start_date=start_date)
        return Response(status=status.HTTP_201_CREATED)

class FarmDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET farms/:id
    PUT farms/:id
    DELETE farms/:id
    """
    queryset = Farm.objects.all()
    serializer_class = FarmsSelializer

    def get(self, request, *args, **kwargs):
        try:
            farm = Farm.objects.get(pk=kwargs['pk'])
            return Response(FarmsSelializer(farm).data)
        
        except Farm.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "farm with id {} does not exist".format(kwargs['pk'])
                }
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            farm = Farm.objects.get(pk=kwargs['pk'])
            serializer = FarmsSelializer()
            update_farm = serializer.update(farm, request.data)
            return Response(FarmsSelializer(farm).data)
        
        except Farm.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "farm with id {} does not exist".format(kwargs['pk'])
                }
            )

    def delete(self, request, *args, **kwargs):
        try:
            farm = self.queryset.get(pk=kwargs['pk'])
            farm.delete()
            return Response(status.HTTP_204_NO_CONTENT)

        except Farm.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "farm with id {} does not exist".format(kwargs['pk'])
                }
            )