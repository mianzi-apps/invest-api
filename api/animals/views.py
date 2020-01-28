from django.shortcuts import render
from rest_framework import generics

class AnimalCreateAPIView(generics.ListCreateAPIView):
    pass


class AnimalDetails(generics.RetrieveUpdateDestroyAPIView):
    pass