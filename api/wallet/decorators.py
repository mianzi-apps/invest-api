from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        user_id = args[0].request.data.get("user_id", '')
        bal = args[0].request.data.get("bal", '')

        if not bal and not user_id:
            return Response(
                data={
                    "message": "bal and user_id are all required to create a wallet"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
