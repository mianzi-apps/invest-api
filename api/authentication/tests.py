from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status
from django.contrib.auth.models import User
import json
# tests for views.

class AuthBaseTest(APITestCase):
    client = APIClient()

    def login_user(self, username="", password=""):
        url = reverse(
            "auth-login",
            kwargs={
                'version':'v1'
            }
        )
        return self.client.post(url,
        data=json.dumps({
            'username': username,
            'password': password
        }),
        content_type="application/json"
        )

    def setUp(self):
        # add test data
        
        # create a admin user
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )

class AuthLoginTest(AuthBaseTest):
    """
    tests auth/login/ endpoint
    """
    def test_login_user_with_valid_credentials(self):
        response = self.login_user("test_user", 'testing')
        # assert token key exists
        print(response)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_wrong_credentials(self):
        response = self.login_user('anonymus', 'pass')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthRegisterTest(AuthBaseTest):
    """
    tests auth/register endpoint
    """
    def test_register_user_with_valid_data(self):
        url = reverse(
            'auth-register',
            kwargs={
                'version': 'v1'
            }
        )
        response = self.client.post(
            url,
            data=json.dumps({
                'username': 'new_user',
                'email': 'new_user@mail.com',
                'password': 'new_pass',
                'first_name': "test",
                'last_name': "user",
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_register_user_with_invalid_data(self):
        url = reverse(
            'auth-register',
            kwargs={
                'version': 'v1'
            }
        )
        response = self.client.post(
            url,
            data=json.dumps({
                'username': '',
                'email': '',
                'password': ''
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)