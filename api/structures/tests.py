from rest_framework.test import APIClient, APITestCase, force_authenticate
from .models import Structure
from farms.models import Farm, Location
from django.urls import reverse
from .serializers import StructuresSerializer
from rest_framework import status
from authentication.tests import AuthBaseTest
from django.contrib.auth.models import User
import json
import datetime

class BaseTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_structure(alias="",purpose="",capacity=0, dimensions="", setup_cost=0, farm=None):
        Structure.objects.create(
            alias=alias,
            purpose=purpose,
            capacity=capacity, 
            dimensions=dimensions,
            setup_cost=setup_cost,
            farm_id=farm
        )

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        location = Location.objects.create(district='test', city='test city')
        self.farm = Farm.objects.create(
            name='kakiri Farm',
            start_date='2020-06-01',
            location=location
        )
        self.create_structure('Kampala gh', 'vg farming', 700, '30*15', 3000000,self.farm)
        

class StructuresTests(BaseTest):
    def test_list_structures(self):
        url = reverse('structures-list-create', kwargs={'version':'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Structure.objects.all()
        serialized = StructuresSerializer(expected, many=True)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_structure(self):
        url = reverse('structures-list-create', kwargs={'version':'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data = json.dumps({
            "alias":"Kla 001",
            "purpose":"green pepper",
            "capacity":100, 
            "dimensions":"15*50",
            "setup_cost":4000000,
            "farm_id": self.farm.pk
        }),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_structure_details(self):
        url = reverse('structure-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Structure.objects.get(pk=1)
        self.assertEqual(StructuresSerializer(expected).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_structure_details(self):
        url = reverse('structure-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data = json.dumps({
            'alias': 'updated test_structure',
        }),
        content_type='application/json' 
        )

        expected = Structure.objects.get(pk=1)
        self.assertEqual(expected.alias, 'updated test_structure')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_structure_details(self):
        url = reverse('structure-details', kwargs={'version':'v1', 'pk':1})
        structures_before_delete = Structure.objects.all().count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        structures_after_delete = Structure.objects.all().count()
        self.assertNotEqual(structures_before_delete, structures_after_delete)
