from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        title = args[0].request.data.get("name", "")
        start_date = args[0].request.data.get("start_date", "")
        if not title and not start_date:
            return Response(
                data={
                    "message": "Both name and start_date are required to add a song"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated