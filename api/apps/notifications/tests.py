from rest_framework.test import APIClient, APITestCase, force_authenticate
from api.apps.projects.models import Project, ProjectProfile
from api.apps.notifications.models import Notification
from django.urls import reverse
from api.apps.projects.serializers import ProjectsSerializer, ProjectProfileSerializer
from api.apps.notifications.serializers import NotificationSerializer
from rest_framework import status
from api.apps.authentication.tests import AuthBaseTest
from api.apps.authentication.models import User
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
            "project_id": project.pk,
            "project_stage": stage,
            "stage_caption": caption,
            "detailed_explanation": explanation,
            "images": images
        }

        serialiser = ProjectProfileSerializer(data=data)
        serialiser.is_valid(raise_exception=True)
        return serialiser.save()

    @staticmethod
    def create_notification(profile_id='', text=''):
        Notification.objects.create(
            profile_id=profile_id,
            notification_text=text
        )

    def setUp(self):
        self.user = User.objects.create_superuser(
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
            contact="0750532902"
        )
        images = [
            {
                'image_url': 'jajj.png',
                'image_caption': 'n'
            },
            {
                'image_url': 'jajj.png',
                'image_caption': 'kk'
            },
        ]
        self.project = self.create_project(
            'kla gh 01', 'our first green house', '2020-01-01', '2020-02-02', 90, '2020-02-03')
        self.profile = self.create_project_profile(
            self.project, '2 weeks', 'kla gh 2010', 'non ', images)
        profile_id = ProjectProfile.objects.get(pk=self.profile.pk)
        self.create_notification(profile_id, 'Harvest time')


class NotificationTests(BaseTest):

    def test_list_notifications(self):
        url = reverse('notifications-list-create', kwargs={'version': 'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Notification.objects.all()
        serialized = NotificationSerializer(expected, many=True)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_notification(self):
        url = reverse('notifications-list-create', kwargs={'version': 'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=json.dumps({
            'profile_id': self.profile.pk,
            'notification_text': 'Harvest time',
        }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_notification_details(self):
        url = reverse('notification-details',
                      kwargs={'version': 'v1', 'pk': 1})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Notification.objects.get(pk=1)
        self.assertEqual(NotificationSerializer(expected).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_notification_details(self):
        url = reverse('notification-details',
                      kwargs={'version': 'v1', 'pk': 1})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data=json.dumps({
            'notification_text': 'Harvest is not ready',
        }),
            content_type='application/json'
        )
        expected = Notification.objects.get(pk=1)
        self.assertEqual(expected.notification_text, 'Harvest is not ready')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_notification(self):
        url = reverse('notification-details',
                      kwargs={'version': 'v1', 'pk': 1})
        notification_before_delete = Notification.objects.all().count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        notification_after_delete = Notification.objects.all().count()
        self.assertNotEqual(notification_before_delete,
                            notification_after_delete)
