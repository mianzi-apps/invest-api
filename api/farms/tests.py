from rest_framework.test import APIClient, APITestCase, force_authenticate
from .models import Location, Farm
from django.urls import reverse
from .selializers import FarmsSelializer, LocationSerializer 
from rest_framework import status
from authentication.tests import AuthBaseTest
from django.contrib.auth.models import User
import json
import datetime

class BaseTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_location(district='', city=''):
        Location.objects.create(
            district=district,
            city=city
        )

    @staticmethod
    def create_farm(name='', start_date='', location=None):
        Farm.objects.create(
            name=name,
            start_date=start_date,
            location=location
        )

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )

        self.create_location('wakiso', 'kakiri')
        self.create_location('kampala', 'kasangati')
        self.location = Location.objects.get(pk=1)
        self.create_farm('kakiri Farm', '2020-06-01', self.location)


class FarmsTests(BaseTest):
    
    def test_list_farms(self):
        url = reverse('farms-list-create', kwargs={'version':'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Farm.objects.all()
        serialized = FarmsSelializer(expected, many=True)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_farm(self):
        url = reverse('farms-list-create', kwargs={'version':'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data = json.dumps({
            'name': 'test farm',
            'start_date': '2020-06-01',
            'location': self.location.pk
        }),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_farm_details(self):
        url = reverse('farm-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Farm.objects.get(pk=1)
        self.assertEqual(FarmsSelializer(expected).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_farm_details(self):
        url = reverse('farm-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data = json.dumps({
            'name': 'updated test_farm',
        }),
        content_type='application/json' 
        )

        expected = Farm.objects.get(pk=1)
        self.assertEqual(expected.name, 'updated test_farm')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_farm_details(self):
        url = reverse('farm-details', kwargs={'version':'v1', 'pk':1})
        farms_before_delete = Farm.objects.all().count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        farms_after_delete = Farm.objects.all().count()
        self.assertNotEqual(farms_before_delete, farms_after_delete)
        # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LocationsTests(BaseTest):
    def test_list_locations(self):
        url = reverse('locations-list-create', kwargs={'version':'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Location.objects.all()
        serialized = LocationSerializer(expected, many=True)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_location(self):
        url = reverse('locations-list-create', kwargs={'version':'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data = json.dumps({
            'district': 'bushenyi',
            'city': 'ishaka',
            'latitude': '0',
            'longitude': '0'
        }),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_location_details(self):
        url = reverse('location-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Location.objects.get(pk=1)
        self.assertEqual(LocationSerializer(expected).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_location_details(self):
        url = reverse('location-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data = json.dumps({
            'district': 'updated location_district',
        }),
        content_type='application/json' 
        )

        expected = Location.objects.get(pk=1)
        self.assertEqual(expected.district, 'updated location_district')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_farm_details(self):
        url = reverse('location-details', kwargs={'version':'v1', 'pk':1})
        locations_before_delete = Location.objects.all().count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        locations_after_delete = Location.objects.all().count()
        self.assertNotEqual(locations_before_delete, locations_after_delete)