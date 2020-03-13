from rest_framework import serializers
from api.apps.transactions.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount','date','type','status')