from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from api.apps.plants.decorators import validate_plant_data
from api.apps.plants.models import Plant
from api.apps.plants.serializers import PlantSerializer


class PlantListCreateAPIView(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    @validate_plant_data
    def post(self, request, *args, **kwargs):
        english_name = request.data.get('english_name', '')
        scientific_name = request.data.get('scientific_name', '')
        estimated_maturity_period = request.data.get('estimated_maturity_period', 0)

        Plant.objects.create(
            english_name=english_name,
            scientific_name=scientific_name,
            estimated_maturity_period=estimated_maturity_period
        )
        return Response(status=status.HTTP_201_CREATED)


class PlantDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    def get(self, request, *args, **kwargs):
        try:
            plant = Plant.objects.get(pk=kwargs['pk'])
            return Response(data=PlantSerializer(plant).data, status=status.HTTP_200_OK)
        except Plant.DoesNotExist:
            return Response(data={
                "message": 'plant with id {} does not exist'.format(kwargs['pk'])
            })

    @validate_plant_data
    def put(self, request, *args, **kwargs):
        try:
            plant = Plant.objects.get(pk=kwargs['pk'])
            serializer = PlantSerializer()
            updated_plant = serializer.update(plant, request.data)
            return Response(data=PlantSerializer(updated_plant).data, status=status.HTTP_200_OK)
        except Plant.DoesNotExist:
            return Response(data={
                "message": 'plant with id {} does not exist'.format(kwargs['pk'])
            })

    def delete(self, request, *args, **kwargs):
        try:
            plant = Plant.objects.get(pk=kwargs['pk'])
            plant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Plant.DoesNotExist:
            return Response(data={
                "message": 'plant with id {} does not exist'.format(kwargs['pk'])
            })
