from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from .models import Animal
from .serializers import AnimalSerializer
from .decorators import validate_animal_data

# Get the JWT settings
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class AnimalListCreateAPIView(generics.ListCreateAPIView):
    """
    GET animals/
    POST animals/
    """
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    @validate_animal_data
    def post(self, request, *args, **kwargs):
        english_name = request.data.get('english_name','')
        scientific_name = request.data.get('scientific_name', '')
        estimated_maturity_period = request.data.get('estimated_maturity_period', 0)
        
        Animal.objects.create(
            english_name=english_name,
            scientific_name=scientific_name,
            estimated_maturity_period=estimated_maturity_period
        )
        return Response(status=status.HTTP_201_CREATED)


class AnimalDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get(self, request, *args, **kwargs):
        try:
            animal = Animal.objects.get(pk=kwargs['pk'])
            return Response(data=AnimalSerializer(animal).data, status=status.HTTP_200_OK)
        except Animal.DoesNotExist:
            return Response(data={
                "message": 'animal with id {} does not exist'.format(kwargs['pk'])
            })

    @validate_animal_data
    def put(self, request, *args, **kwargs):
        try:
            animal = Animal.objects.get(pk=kwargs['pk'])
            serializer = AnimalSerializer()
            updated_animal= serializer.update(animal, request.data)
            return Response(data=AnimalSerializer(updated_animal).data, status=status.HTTP_200_OK)
        except Animal.DoesNotExist:
            return Response(data={
                "message": 'animal with id {} does not exist'.format(kwargs['pk'])
            })


    def delete(self, request, *args, **kwargs):
        try:
            animal = Animal.objects.get(pk=kwargs['pk'])
            animal.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Animal.DoesNotExist:
            return Response(data={
                "message": 'animal with id {} does not exist'.format(kwargs['pk'])
            })