from rest_framework import serializers
from api.apps.authentication.models import User


class TokenSerializer(serializers.Serializer):
    """
    this serializer serialises token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.Serializer):

    class Meta:
        model = User,
        fields = ('first_name', 'last_name', 'email',
                  'contact', 'username', 'password')
