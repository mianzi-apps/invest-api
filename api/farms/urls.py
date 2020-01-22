# urls.py file in the posts folder
from django.urls import path
from .views import FarmDetailsView, ListCreateFarmsView

urlpatterns = [
    path('farms/', ListCreateFarmsView.as_view(), name="farms-list-create"),
    path('farms/<int:pk>', FarmDetailsView.as_view(), name="farm-details"),
]
