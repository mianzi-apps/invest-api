from rest_framework import generics, permissions
from rest_framework.views import Response, status
from rest_framework_jwt.settings import api_settings

from api.apps.farms.models import Farm
from api.apps.structures.decorators import validate_request_data
from api.apps.structures.models import Structure
from api.apps.structures.serializers import StructuresSerializer

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class StructuresListCreateView(generics.ListCreateAPIView):
    """
    GET structures/
    POST structures/
    """
    queryset = Structure.objects.all()
    serializer_class = StructuresSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        alias = request.data.get("alias", "")
        purpose = request.data.get("purpose", "")
        capacity = request.data.get("capacity", 0)
        dimensions = request.data.get("dimensions", "")
        setup_cost = request.data.get("setup_cost", 0)
        farm_id = request.data.get("farm_id", '')

        Structure.objects.create(alias=alias,
                                 purpose=purpose,
                                 capacity=capacity,
                                 dimensions=dimensions,
                                 setup_cost=setup_cost,
                                 farm_id=Farm.objects.get(pk=farm_id)
                                 )
        return Response(status=status.HTTP_201_CREATED)


class StructuresDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET structures/:id
    PUT structures/:id
    DELETE structures/:id
    """
    queryset = Structure.objects.all()
    serializer_class = StructuresSerializer

    def get(self, request, *args, **kwargs):
        try:
            structure = Structure.objects.get(pk=kwargs['pk'])
            return Response(StructuresSerializer(structure).data)

        except Structure.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "structure with id {} does not exist".format(kwargs['pk'])
                }
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            structure = Structure.objects.get(pk=kwargs['pk'])
            serializer = StructuresSerializer()
            update_farm = serializer.update(structure, request.data)
            return Response(StructuresSerializer(structure).data)

        except Structure.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "structure with id {} does not exist".format(kwargs['pk'])
                }
            )

    def delete(self, request, *args, **kwargs):
        try:
            structure = self.queryset.get(pk=kwargs['pk'])
            structure.delete()
            return Response(status.HTTP_204_NO_CONTENT)

        except Structure.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "structure with id {} does not exist".format(kwargs['pk'])
                }
            )
