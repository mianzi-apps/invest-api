from django.urls import path

from api.apps.projects.views import (ProjectListCreateAPIView,
                                     ProjectDetailsView,
                                     ProjectProfileListCreateAPIView,
                                     ProjectProfileDetails,
                                     ProfileImagesCreateAPIView,
                                     ProfileImagesDestroyView,
                                     ProjectPlantCreateAPIView,
                                     ProjectPlantDestroyView,
                                     ProjectAnimalCreateAPIView,
                                     ProjectAnimalDestroyView,
                                     ProjectExpensesListCreateAPIView,
                                     ProjectExpensesDetails,
                                     ProjectEarningsListCreateAPIView,
                                     ProjectEarningsDetails
                                     )

urlpatterns = [
    path('projects/', ProjectListCreateAPIView.as_view(), name='projects-list-create'),
    path('projects/<int:pk>', ProjectDetailsView.as_view(), name='project-details'),
    path('profiles/<int:pk>', ProjectProfileListCreateAPIView.as_view(), name='project-profiles-list-create'),
    path('profile/<int:pk>', ProjectProfileDetails.as_view(), name='project-profile-details'),
    path('profile/image/<int:pk>', ProfileImagesCreateAPIView.as_view(), name='profile-image-add'),
    path('profile/image/<int:pk>', ProfileImagesDestroyView.as_view(), name='profile-image-remove'),
    path('project/plant/<int:pk>', ProjectPlantCreateAPIView.as_view(), name='project-plant-add'),
    path('project/plant/<int:pk>', ProjectPlantDestroyView.as_view(), name='project-plant-remove'),
    path('project/animal/<int:pk>', ProjectAnimalCreateAPIView.as_view(), name='project-animal-add'),
    path('project/animal/<int:pk>', ProjectAnimalDestroyView.as_view(), name='project-animal-remove'),
    path('project/earnings/<int:pk>', ProjectEarningsListCreateAPIView.as_view(), name='project-earning-list-create'),
    path('project/earning/<int:pk>', ProjectEarningsDetails.as_view(), name="project-earning-details"),
    path('project/expenses/<int:pk>', ProjectExpensesListCreateAPIView.as_view(), name="project-expense-list-create"),
    path('project/expense/<int:pk>', ProjectExpensesDetails.as_view(), name="project-expense-details")
]
