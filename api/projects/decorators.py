from rest_framework.response import Response
from rest_framework import status

def validated_data(fn):
    def decorator(*args, **kwargs):
        alias = args[0].request.data.get('alias', '')
        description = args[0].request.data.get('description', '')
        start_date = args[0].request.data.get('start_date', '')
        harvest_start_date = args[0].request.data.get('harvest_start_date', '')
        estimated_harvest_duration = args[0].request.data.get('estimated_harvest_duration', '')

        if not alias and not description and not start_date and not harvest_start_date and not estimated_harvest_duration:
            return Response(data={
                'message': 'alias, description, start_date, harvest_start_date, estimated_harvest_duration are required'
            }, status=status.HTTP_400_BAD_REQUEST
            )
        
        return fn(*args, **kwargs)
    return decorator