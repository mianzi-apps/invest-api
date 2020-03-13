from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        alias = args[0].request.data.get("alias", "")
        purpose = args[0].request.data.get("purpose", "")
        capacity = args[0].request.data.get("capacity", 0)
        dimensions = args[0].request.data.get("dimensions", "")
        setup_cost = args[0].request.data.get("setup_cost", 0)
        farm_id = args[0].request.data.get("farm_id", '')
        if not alias and not purpose and not capacity and not dimensions and not setup_cost and not farm_id:
            return Response(
                data={
                    "message": "alias,purpose,capacity, dimensions, setup_cost are all required to create a structure"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorated
