from django.urls import path
from .views import (ProjectListCreateAPIView,
                    ProjectDetailsView, 
                    ProjectProfileListCreateAPIView, 
                    ProjectProfileDetails,
                    ProfileImagesCreateAPIView, 
                    ProfileImagesDestroyView,
                    ProjectPlantCreateAPIView,
                    ProjectPlantDestroyView,
                    ProjectAnimalCreateAPIView,
                    ProjectAnimalDestroyView
                    )

urlpatterns =[
    path('projects/', ProjectListCreateAPIView.as_view(), name='projects-list-create'),
    path('projects/<int:pk>', ProjectDetailsView.as_view(), name='project-details'),
    path('profiles/<int:pk>', ProjectProfileListCreateAPIView.as_view(), name='project-profiles-list-create'),
    path('profile/<int:pk>', ProjectProfileDetails.as_view(),  name='project-profile-details'),
    path('profile_image/<int:pk>', ProfileImagesCreateAPIView.as_view(), name='profile-image-add'),
    path('profile_image/<int:pk>', ProfileImagesDestroyView.as_view(), name='profile-image-remove'),
    path('project_plant/<int:pk>', ProjectPlantCreateAPIView.as_view(), name='project-plant-add'),
    path('project_plant/<int:pk>', ProjectPlantDestroyView.as_view(), name='project-plant-remove'),
    path('project_animal/<int:pk>', ProjectAnimalCreateAPIView.as_view(), name='project-animal-add'),
    path('project_animal/<int:pk>', ProjectAnimalDestroyView.as_view(), name='project-animal-remove'),
]