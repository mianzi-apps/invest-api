from rest_framework.test import APIClient, APITestCase, force_authenticate
from .models import Wallet
from django.contrib.auth.models import User
from django.urls import reverse
from .serializers import WalletSerializer
from rest_framework import status
from authentication.tests import AuthBaseTest
import json




class BaseTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_wallet(user_id="",bal=""):
        Wallet.objects.create(
            user_id=user_id,
            bal=bal
        )

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        user =User.objects.get(pk=self.user.pk)
        self.create_wallet(user,300.0)


class WalletTests(BaseTest):
    def test_list_wallet(self):
        url = reverse('wallet-list-create', kwargs={'version': 'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Wallet.objects.all()
        serialized = WalletSerializer(expected, many=True)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_wallet(self):
        url = reverse('wallet-list-create', kwargs={'version': 'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=json.dumps({
            "user_id":self.user.pk,
            "bal": 400.0,
        }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_wallet_details(self):
        url = reverse('wallet-details', kwargs={'version': 'v1', 'pk': 1})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Wallet.objects.get(pk=1)
        self.assertEqual(WalletSerializer(expected).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wallet_details(self):
        url = reverse('wallet-details', kwargs={'version': 'v1', 'pk': 1})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data=json.dumps({
            'bal': 6000.0,
        }),
            content_type='application/json'
        )

        expected = Wallet.objects.get(pk=1)
        self.assertEqual(expected.bal, 6000.0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_wallet_details(self):
        url = reverse('wallet-details', kwargs={'version': 'v1', 'pk': 1})
        wallet_before_delete = Wallet.objects.all().count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        wallet_after_delete = Wallet.objects.all().count()
        self.assertNotEqual(wallet_before_delete, wallet_after_delete)
