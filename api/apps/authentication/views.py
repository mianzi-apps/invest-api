from django.shortcuts import render
from django.contrib.auth import authenticate, login
from api.apps.authentication.models import User
from rest_framework import generics
from api.apps.authentication.serializers import TokenSerializer, UserSerializer
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from rest_framework.views import status, Response

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.
class LoginView(generics.CreateAPIView):
    """
    Post auth/login
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', "")
        password = request.data.get('password', "")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # login saves the user id in the session
            # using django's session framework
            login(request, user)
            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(jwt_payload_handler(user))
            })
            serializer.is_valid()
            return Response(serializer.data)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(generics.CreateAPIView):
    """
    Post auth/register
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        password = request.data.get('password', "")
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        email = request.data.get('email', "")
        contact = request.data.get('contact', "")

        if not password or not email or not first_name or not last_name or not contact:
            return Response(data={
                "massage": " password, first_name, last_name, email and contact is required to register a user"
            }, status=status.HTTP_400_BAD_REQUEST)
        new_user = User.objects.create_user(
                                password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            contact=contact,
                                            )
        return Response(status=status.HTTP_201_CREATED)
