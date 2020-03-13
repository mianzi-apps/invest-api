from rest_framework import generics, permissions
from rest_framework.views import Response, status
from rest_framework_jwt.settings import api_settings

from api.apps.authentication.models import User
from api.apps.wallet.decorators import validate_request_data
from api.apps.wallet.models import Wallet
from api.apps.wallet.serializers import WalletSerializer

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class WalletListView(generics.ListCreateAPIView):
    """
    GET wallets/
    POST wallet/
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', '')
        balance = request.data.get('balance', '')

        Wallet.objects.create(user_id=User.objects.get(pk=user_id),
                              balance=balance)
        return Response(status=status.HTTP_201_CREATED)


class WalletDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET wallet/:id
    PUT wallet/:id
    DELETE wallet/:id
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated,)

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
