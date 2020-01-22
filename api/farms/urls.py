# urls.py file in the posts folder
from django.urls import path
from .views import FarmDetailsView, ListCreateFarmsView, ListCreateLocationsView, LocationDetails

urlpatterns = [
    path('farms/', ListCreateFarmsView.as_view(), name="farms-list-create"),
    path('farms/<int:pk>', FarmDetailsView.as_view(), name="farm-details"),
    path('locations/', ListCreateLocationsView.as_view(), name="locations-list-create"),
    path('locations/<int:pk>', LocationDetails.as_view(), name="location-details"),
]
