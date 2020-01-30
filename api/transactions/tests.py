from rest_framework.test import APIClient, APITestCase, force_authenticate
from .models import Transaction
from django.urls import reverse
from .serializers import TransactionSerializer
from rest_framework import status
from authentication.tests import AuthBaseTest
from django.contrib.auth.models import User
import json


class BaseTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_transaction(amount='', type='', status="",):
        Transaction.objects.create(
            amount=amount,
            type=type,
            status=status
        )

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )

        self.create_transaction(300.00, 'deposit', 'pending')


class TransactionTests(BaseTest):

    def test_list_transactions(self):
        url = reverse('transactions-list-create', kwargs={'version': 'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Transaction.objects.all()
        serialized = TransactionSerializer(expected, many=True)
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_transaction(self):
        url = reverse('transactions-list-create', kwargs={'version': 'v1'})
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=json.dumps({
            'amount': 3000.00,
            'type': 'deposit',
            'status': 'pending',
        }),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_transaction_details(self):
        url = reverse('transaction-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        expected = Transaction.objects.get(pk=1)
        self.assertEqual(TransactionSerializer(expected).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_transaction_details(self):
        url = reverse('transaction-details', kwargs={'version':'v1', 'pk':1})
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data = json.dumps({
            'amount': 7000.00,
        }),
        content_type='application/json' 
        )
        expected = Transaction.objects.get(pk=1)
        self.assertEqual(expected.amount, 7000.00)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_transaction(self):
        url = reverse('transaction-details', kwargs={'version':'v1', 'pk':1})
        transactions_before_delete = Transaction.objects.all().count()
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        transactions_after_delete = Transaction.objects.all().count()
        self.assertNotEqual(transactions_before_delete, transactions_after_delete)

