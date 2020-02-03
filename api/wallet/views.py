from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import Response, status
from .serializers import WalletSerializer
from .models import Wallet
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from .decorators import validate_request_data



# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.


class WalletListView(generics.ListCreateAPIView):
    """
    GET wallets/
    POST wallet/
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @validate_request_data
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', '')
        bal = request.data.get('bal', '')

        Wallet.objects.create(user_id=User.objects.get(pk=user_id),
                            bal=bal)
        return Response(status=status.HTTP_201_CREATED)


class WalletDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET wallet/:id
    PUT wallet/:id
    DELETE wallet/:id
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(pk=kwargs['pk'])
            return Response(WalletSerializer(wallet).data)

        except Wallet.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "wallet with id {} does not exist".format(kwargs['pk'])
                }
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(pk=kwargs['pk'])
            serializer = WalletSerializer()
            update_wallet = serializer.update(wallet, request.data)
            return Response(WalletSerializer(wallet).data)

        except Wallet.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "wallet with id {} does not exist".format(kwargs['pk'])
                }
            )

    def delete(self, request, *args, **kwargs):
        try:
            wallet = self.queryset.get(pk=kwargs['pk'])
            wallet.delete()
            return Response(status.HTTP_204_NO_CONTENT)

        except Wallet.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "message": "wallet with id {} does not exist".format(kwargs['pk'])
                }
            )
