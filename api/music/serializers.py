from rest_framework import serializers
from .models import Songs

class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ('title', 'artist')
        
class TokenSerializer(serializers.Serializer):
    """
    this serializer serialises token data
    """
    token = serializers.CharField(max_length=255)
    