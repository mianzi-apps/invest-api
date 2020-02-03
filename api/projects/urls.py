from django.urls import path
from .views import (ProjectListCreateAPIView,
                    ProjectDetailsView, 
                    ProjectProfileListCreateAPIView, 
                    ProjectProfileDetails,
                    ProfileImagesCreateAPIView, 
                    ProfileImagesDestroyView)

urlpatterns =[
    path('projects/', ProjectListCreateAPIView.as_view(), name='projects-list-create'),
    path('projects/<int:pk>', ProjectDetailsView.as_view(), name='project-details'),
    path('profiles/<int:pk>', ProjectProfileListCreateAPIView.as_view(), name='project-profiles-list-create'),
    path('profile/<int:pk>', ProjectProfileDetails.as_view(),  name='project-profile-details'),
    path('profile_image/<int:pk>', ProfileImagesCreateAPIView.as_view(), name='profile-image-add'),
    path('profile_image/<int:pk>', ProfileImagesDestroyView.as_view(), name='profile-image-remove')
]