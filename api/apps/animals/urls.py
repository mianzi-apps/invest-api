from django.urls import path

from api.apps.animals.views import AnimalListCreateAPIView, AnimalDetailsAPIView

urlpatterns = [
    path('animals/', AnimalListCreateAPIView.as_view(), name='animals-list-create'),
    path('animals/<int:pk>', AnimalDetailsAPIView.as_view(), name='animal-details')
]
