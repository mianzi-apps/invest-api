from django.shortcuts import render
from rest_framework import generics

class PlantCreateAPIView(generics.ListCreateAPIView):
    pass


class PlantDetails(generics.RetrieveUpdateDestroyAPIView):
    pass
