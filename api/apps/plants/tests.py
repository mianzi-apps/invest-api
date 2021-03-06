import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.apps.authentication.models import User
from api.apps.plants.models import Plant
from api.apps.plants.serializers import PlantSerializer


class BaseTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_plant(eng_name='', sci_name='', maturity=0):
        return Plant.objects.create(
            english_name=eng_name,
            scientific_name=sci_name,
            estimated_maturity_period=maturity
        )

    def setUp(self):
        self.user = User.objects.create_superuser(
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
            contact="0750532902"
        )
        self.create_plant('Sweet Pepper', 'Sweet pepper', 90)
        self.create_plant('Tomatoes', 'Tomatoes', 90)


class PlantTests(BaseTest):

    def test_list_plants(self):
        url = reverse('plants-list-create', kwargs={'version': 'v1'})
        self.client.force_authenticate(user=self.user)
        expected = Plant.objects.all()
        response = self.client.get(url)
        serialized = PlantSerializer(expected, many=True)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_Plant(self):
        url = reverse('plants-list-create', kwargs={'version': 'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=json.dumps({
            'english_name': 'rabbit',
            'scientific_name': 'not known',
            'estimated_maturity_period': 50,
        }),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_plant_details(self):
        url = reverse('plant-details', kwargs={'version': 'v1', 'pk': 1})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Plant.objects.get(pk=1)
        self.assertEqual(PlantSerializer(expected).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_plant_details(self):
        url = reverse('plant-details', kwargs={'version': 'v1', 'pk': 1})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data=json.dumps({
            'english_name': 'updated plant name',
        }),
                                   content_type='application/json'
                                   )
        expected = Plant.objects.get(pk=1)
        self.assertEqual(expected.english_name, 'updated plant name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_plant(self):
        url = reverse('plant-details', kwargs={'version': 'v1', 'pk': 1})
        plants_before_delete = Plant.objects.all().count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        plants_after_delete = Plant.objects.all().count()
        self.assertNotEqual(plants_before_delete, plants_after_delete)
