from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer
from projects.models import ProjectProfile
from rest_framework_jwt.settings import api_settings
from .decorators import validated_data
from rest_framework.response import Response
from rest_framework import status


# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class NotificationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated, )

    @validated_data
    def post(self, request, *args, **kwargs):
        profile_id = request.data.get('profile_id', '')
        notification_text = request.data.get('notification_text', '')

        Notification.objects.create(
            profile_id=ProjectProfile.objects.get(pk=profile_id),
            notification_text=notification_text
        )
        return Response(status=status.HTTP_201_CREATED)


class NotificationDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            notification = Notification.objects.get(pk=kwargs['pk'])
            return Response(data=NotificationSerializer(notification).data, status=status.HTTP_200_OK)

        except Notification.DoesNotExist:
            return Response(data={
                'message': 'notification with id {} was not found'.format(kwargs['pk'])
            })

    @validated_data
    def put(self, request, *args, **kwargs):
        try:
            notification = Notification.objects.get(pk=kwargs['pk'])
            serializer = NotificationSerializer()
            update_notification = serializer.update(notification, request.data)
            return Response(data=NotificationSerializer(notification).data, status=status.HTTP_200_OK)

        except Notification.DoesNotExist:
            return Response(data={
                'message': 'notification with id {} was not found'.format(kwargs['pk'])
            })

    def delete(self, request, *args, **kwargs):
        try:
            notification = Notification.objects.get(pk=kwargs['pk'])
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Notification.DoesNotExist:
            return Response(data={
                'message': 'notification with id {} was not found'.format(kwargs['pk'])
            })