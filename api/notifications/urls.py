from django.urls import path
from .views import NotificationListCreateAPIView, NotificationDetailsView


urlpatterns =[
    path('notifications/' , NotificationListCreateAPIView.as_view(), name='notifications-list-create'),
    path('notifications/<int:pk>' , NotificationDetailsView.as_view(), name='notification-details'),
]