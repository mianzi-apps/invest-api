from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    """
    this serializer serialises token data
    """
    token = serializers.CharField(max_length=255)
    