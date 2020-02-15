from django.db import models
from api.apps.projects.models import ProjectProfile

class Notification(models.Model):
    profile_id = models.ForeignKey(ProjectProfile, on_delete=models.CASCADE)
    notification_text = models.CharField(max_length=200)
