from rest_framework import status
from rest_framework.response import Response


def validated_data(fn):
    def decorator(*args, **kwargs):
        profile_id = args[0].request.data.get('profile_id', '')
        notification_text = args[0].request.data.get('notification_text', '')

        if not profile_id and not notification_text:
            return Response(data={
                'message': 'profile_id and notification_text  are required'
            }, status=status.HTTP_400_BAD_REQUEST
            )

        return fn(*args, **kwargs)

    return decorator
