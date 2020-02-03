from rest_framework.test import APIClient, APITestCase, force_authenticate
from .models import Project, ProjectProfile
from django.urls import reverse
from .serializers import ProjectsSerializer, ProjectProfileSerializer
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
        return Project.objects.create(
            alias=alias, 
            description=description, 
            start_date=start_date,
            harvest_start_date=harvest_start_date, 
            estimated_harvest_duration=estimated_harvest_duration, 
            actual_harvest_end_date=actual_harvest_end_date
        )

    @staticmethod
    def create_project_profile(project=None, stage='', caption='', explanation='', images=[]):
        data = {
            "project_id":project.pk,
            "project_stage":stage,
            "stage_caption":caption,
            "detailed_explanation":explanation,
            "images":images
        }
        
        serialiser = ProjectProfileSerializer(data=data)
        serialiser.is_valid(raise_exception=True)
        serialiser.save()
        

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        images =[
            {
                'image_url':'jajj.png',
                'image_caption':'n'
            },
            {
                'image_url':'jajj.png',
                'image_caption':'kk'
            },
        ]
        self.project=self.create_project('kla gh 01', 'our first green house', '2020-01-01', '2020-02-02', 90, '2020-02-03')
        self.create_project_profile(self.project, '2 weeks', 'kla gh 2010', 'non ', images)
        self.create_project_profile(self.project, '3 weeks', 'kla gh 2011', 'non2 ', images)

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


class ProjectProfilesTests(BaseTest):

    def test_profile_list(self):
        url = reverse('project-profiles-list-create', kwargs={'version':'v1', 'pk':self.project.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = ProjectProfile.objects.filter(project_id=self.project)
        serialized = ProjectProfileSerializer(expected, many=True)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_create(self):
        url = reverse('project-profiles-list-create', kwargs={'version':'v1', 'pk':self.project.pk})
        self.client.force_authenticate(user=self.user)
        data = json.dumps({
            "project_id":self.project.pk,
            "project_stage":'4 weeks',
            "stage_caption": 'typically fruiting stage',
            "detailed_explanation": 'none',
            "images":[{
                'image_url':'love.png',
                'image_caption':'love me'
            }
            ]
        })
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_profile_update(self):
        url = reverse('project-profile-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        data = json.dumps({
            "project_stage":'5 weeks new update',
        })
        response = self.client.put(url, data=data, content_type='application/json')
        updated_project = ProjectProfile.objects.get(pk=1)
        self.assertEqual(updated_project.project_stage,'5 weeks new update')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_details(self):
        url = reverse('project-profile-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_delete(self):
        url = reverse('project-profile-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        profiles_before = ProjectProfile.objects.filter(project_id=1).count()
        response = self.client.delete(url)
        profiles_after = ProjectProfile.objects.filter(project_id=1).count()
        self.assertNotEqual(profiles_after,profiles_before)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_profile_image(self):
        url = reverse('profile-image-add', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        data = json.dumps({
            "image_url":'like.png',
            'image_caption': 'our week 5 image'
        })
        before_profile = ProjectProfile.objects.get(pk=1)
        response = self.client.post(url, data=data, content_type='application/json')
        new_profile = ProjectProfile.objects.get(pk=1)
        self.assertNotEqual(before_profile.images.count,new_profile.images.count)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_profile_image(self):
        url = reverse('profile-image-remove', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        before_profile = ProjectProfile.objects.get(pk=1)
        response = self.client.delete(url)
        new_profile = ProjectProfile.objects.get(pk=1)
        self.assertNotEqual(before_profile.images.count,new_profile.images.count)
