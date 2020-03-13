from rest_framework.test import APIClient, APITestCase, force_authenticate
from api.apps.animals.models import Animal
from django.urls import reverse
from api.apps.animals.serializers import AnimalSerializer
from rest_framework import status
from api.apps.authentication.tests import AuthBaseTest
from api.apps.authentication.models import User
import json
import datetime

class BaseTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_animal(eng_name='', sci_name='', maturity=0):
        return Animal.objects.create(
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
        self.create_animal('Pig', 'Pig', 180)
        self.create_animal('Goat', 'Goat', 280)

class AnimalTests(BaseTest):
    
    def test_list_animals(self):
        url = reverse('animals-list-create', kwargs={'version':'v1'})
        self.client.force_authenticate(user=self.user)
        expected = Animal.objects.all()
        response = self.client.get(url)
        serialized = AnimalSerializer(expected, many=True)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_animal(self):
        url = reverse('animals-list-create', kwargs={'version':'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data = json.dumps({
            'english_name':'rabbit', 
            'scientific_name':'not known', 
            'estimated_maturity_period':50,
        }),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_animal_details(self):
        url = reverse('animal-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Animal.objects.get(pk=1)
        self.assertEqual(AnimalSerializer(expected).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_animal_details(self):
        url = reverse('animal-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data = json.dumps({
            'english_name': 'updated rabbit name',
        }),
        content_type='application/json' 
        )
        expected = Animal.objects.get(pk=1)
        self.assertEqual(expected.english_name, 'updated rabbit name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_animal(self):
        url = reverse('animal-details', kwargs={'version':'v1', 'pk':1})
        animals_before_delete = Animal.objects.all().count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        animals_after_delete = Animal.objects.all().count()
        self.assertNotEqual(animals_before_delete, animals_after_delete)
