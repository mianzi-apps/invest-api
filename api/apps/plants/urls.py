from django.urls import path

from api.apps.plants.views import PlantListCreateAPIView, PlantDetailsAPIView

urlpatterns = [
    path('plants/', PlantListCreateAPIView.as_view(), name='plants-list-create'),
    path('plants/<int:pk>', PlantDetailsAPIView.as_view(), name='plant-details')
]
