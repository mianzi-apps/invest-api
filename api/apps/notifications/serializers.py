from rest_framework import serializers
from api.apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('profile_id', 'notification_text')
