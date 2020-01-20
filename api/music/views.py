from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import generics
from .models import Songs
from .serializers import SongsSerializer, TokenSerializer
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from rest_framework.views import status, Response


# Create your views here.
class ListSongsView(generics.ListAPIView):
    """
    provides a get method handler
    """
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    permission_class = (permissions.IsAuthenticated, )
    
