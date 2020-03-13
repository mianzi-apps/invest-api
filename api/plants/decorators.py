from rest_framework.response import Response
from rest_framework import status

def validate_plant_data(fn):
    def decorator(*args, **kwargs):
        english_name = args[0].request.data.get('english_name','')
        scientific_name = args[0].request.data.get('scientific_name', '')
        estimated_maturity_period = args[0].request.data.get('estimated_maturity_period', 0)

        if not english_name and not scientific_name and not estimated_maturity_period:
            return Response(
                data={'message':'english_name, scientific_name and estimated_maturity_period are required'}, 
                status=status.HTTP_400_BAD_REQUEST)
        return fn(*args, **kwargs)
    return decorator