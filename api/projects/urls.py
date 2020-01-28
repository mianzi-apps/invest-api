from django.urls import path
from .views import ProjectListCreateAPIView, ProjectDetailsView


urlpatterns =[
    path('projects/' , ProjectListCreateAPIView.as_view(), name='projects-list-create'),
    path('projects/<int:pk>' , ProjectDetailsView.as_view(), name='project-details'),
]