from django.db import models
from projects.models import ProjectProfile
# Create your models here.


class Notification(models.Model):
    profile_id = models.ForeignKey(ProjectProfile, on_delete=models.CASCADE)
    notification_text = models.CharField(max_length=200)
