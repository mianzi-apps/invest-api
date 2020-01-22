from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        name = args[0].request.data.get("name", "")
        start_date = args[0].request.data.get("start_date", "")
        if not name and not start_date:
            return Response(
                data={
                    "message": "Both name and start_date are required to add a farm"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated


def validate_location_request_data(fn):
    def decorated(*args, **kwargs):
        district = args[0].request.data.get("district", "")
        city = args[0].request.data.get("city", "")
        latitude = args[0].request.data.get("latitude", "")
        longitude = args[0].request.data.get("longitude", "")

        if not district and not city and not latitude and not longitude:
            return Response(
                data={
                    "message": "district,city, latitude and longitude are required to add a location"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated