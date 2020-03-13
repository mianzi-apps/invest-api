from django.urls import path
from .views import AnimalListCreateAPIView, AnimalDetailsAPIView

urlpatterns = [
    path('animals/', AnimalListCreateAPIView.as_view(), name='animals-list-create'),
    path('animals/<int:pk>', AnimalDetailsAPIView.as_view(), name='animal-details')
]