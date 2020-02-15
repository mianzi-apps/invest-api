from django.shortcuts import render
from rest_framework import generics, permissions
from api.apps.transactions.models import Transaction
from api.apps.transactions.serializers import TransactionSerializer
from rest_framework_jwt.settings import api_settings
from api.apps.transactions.decorators import validated_data
from rest_framework.response import Response
from rest_framework import status


# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @validated_data
    def post(self, request, *args, **kwargs):
        amount = request.data.get('amount', '')
        type = request.data.get('type', '')
        transaction_status = request.data.get('status', '')

        Transaction.objects.create(
            amount=amount,
            type=type,
            status=transaction_status
        )
        return Response(status=status.HTTP_201_CREATED)


class TransactionDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(pk=kwargs['pk'])
            return Response(data=TransactionSerializer(transaction).data, status=status.HTTP_200_OK)

        except Transaction.DoesNotExist:
            return Response(data={
                'message': 'transaction with id {} was not found'.format(kwargs['pk'])
            })

    @validated_data
    def put(self, request, *args, **kwargs):
        try:
            transanction = Transaction.objects.get(pk=kwargs['pk'])
            serializer = TransactionSerializer()
            update_transaction = serializer.update(transanction, request.data)
            return Response(data=TransactionSerializer(transanction).data, status=status.HTTP_200_OK)

        except Transaction.DoesNotExist:
            return Response(data={
                'message': 'transanction with id {} was not found'.format(kwargs['pk'])
            })

    def delete(self, request, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(pk=kwargs['pk'])
            transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Transaction.DoesNotExist:
            return Response(data={
                'message': 'transaction with id {} was not found'.format(kwargs['pk'])
            })
