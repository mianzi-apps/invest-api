from rest_framework.test import APIClient, APITestCase, force_authenticate
from .models import Project
from django.urls import reverse
from .serializers import ProjectsSerializer
from rest_framework import status
from authentication.tests import AuthBaseTest
from django.contrib.auth.models import User
import json
import datetime

class BaseTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_project(alias='', description='', start_date="", harvest_start_date="", 
                estimated_harvest_duration=0, actual_harvest_end_date=""):
        Project.objects.create(
            alias=alias, 
            description=description, 
            start_date=start_date,
            harvest_start_date=harvest_start_date, 
            estimated_harvest_duration=estimated_harvest_duration, 
            actual_harvest_end_date=actual_harvest_end_date
        )

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )

        self.create_project('kla gh 01', 'our first green house', '2020-01-01', '2020-02-02', 90, '2020-02-03' )

class ProjectTests(BaseTest):
    
    def test_list_projects(self):
        url = reverse('projects-list-create', kwargs={'version':'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Project.objects.all()
        serialized = ProjectsSerializer(expected, many=True)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project(self):
        url = reverse('projects-list-create', kwargs={'version':'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data = json.dumps({
            'alias':'alias', 
            'description':'description', 
            'start_date':'2020-01-01',
            'harvest_start_date':'2020-02-02', 
            'estimated_harvest_duration':90, 
            'actual_harvest_end_date':'2020-04-04'
        }),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_project_details(self):
        url = reverse('project-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Project.objects.get(pk=1)
        self.assertEqual(ProjectsSerializer(expected).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_project_details(self):
        url = reverse('project-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data = json.dumps({
            'alias': 'updated test_project',
        }),
        content_type='application/json' 
        )
        expected = Project.objects.get(pk=1)
        self.assertEqual(expected.alias, 'updated test_project')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project(self):
        url = reverse('project-details', kwargs={'version':'v1', 'pk':1})
        projects_before_delete = Project.objects.all().count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        projects_after_delete = Project.objects.all().count()
        self.assertNotEqual(projects_before_delete, projects_after_delete)

