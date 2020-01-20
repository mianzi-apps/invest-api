from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer
from django.contrib.auth.models import User
import json
# tests for views.

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(title="", artist=""):
        if title!="" and artist!="":
            Songs.objects.create(title=title, artist=artist)
    
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
        self.create_song("like glue", "sean paul")
        self.create_song("simple song", "konshens")
        self.create_song("love is wicked", "brick and lace")
        self.create_song("jam rock", "damien marley")
    
class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )
         # fetch the data from db
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AuthLoginTest(BaseViewTest):
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