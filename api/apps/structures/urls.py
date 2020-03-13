from django.urls import path

from api.apps.structures.views import StructuresDetailsView, StructuresListCreateView

urlpatterns = [
    path('structures', StructuresListCreateView.as_view(), name='structures-list-create'),
    path('structures/<int:pk>', StructuresDetailsView.as_view(), name='structure-details'),
]
