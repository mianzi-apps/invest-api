from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import generics
from .models import Songs
from .serializers import SongsSerializer, TokenSerializer
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from rest_framework.views import status, Response

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.
class ListSongsView(generics.ListAPIView):
    """
    provides a get method handler
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    permission_class = (permissions.IsAuthenticated, )
    
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