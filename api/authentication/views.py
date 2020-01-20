from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import TokenSerializer
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

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', "")
        password = request.data.get('password', "")
        user = authenticate(request, username=username, password=password) 

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

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', "")
        password = request.data.get('password', "")
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        email = request.data.get('email', "")

        if not username or not password or not email or not first_name or not last_name:
            return Response(data={
                "massage" : "username, password, first_name, last_name and email is required to register a user"
            }, status=status.HTTP_400_BAD_REQUEST)
        new_user = User.objects.create_user(username=username, 
                                            password=password, 
                                            first_name=first_name, 
                                            last_name=last_name, 
                                            email=email
                                            )
        return Response(status=status.HTTP_201_CREATED)

