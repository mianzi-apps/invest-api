from rest_framework.response import Response
from rest_framework import status

def validated_data(fn):
    def decorator(*args, **kwargs):
        amount = args[0].request.data.get('amount', '')
        type = args[0].request.data.get('type', '')
        status = args[0].request.data.get('status', '')

        if not amount and not type and not status:
            return Response(data={
                'message': 'amount,type and status are required'
            }, status=status.HTTP_400_BAD_REQUEST
            )
        
        return fn(*args, **kwargs)
    return decorator