from django.db import models
from plants.models import Plant
from animals.models import Animal

class Project(models.Model):
    alias = models.CharField(max_length=255)
    description = models.TextField(max_length=400)
    start_date = models.DateField()
    harvest_start_date = models.DateField()
    # no days for which harvest is expected to last
    estimated_harvest_duration = models.IntegerField()
    actual_harvest_end_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class ProjectProfile(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    # this stage can be recorded as text eg 2 weeks, 4 months ....
    project_stage = models.CharField(max_length=255)
    # this could be a small text description for this stage
    stage_caption = models.TextField(max_length=400)
    # this could be used to provide a more detailed explanation for this stage
    detailed_explanation = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class ProjectProfileImages(models.Model):
    profile_id = models.ForeignKey(ProjectProfile, on_delete=models.CASCADE)
    image_url = models.TextField(max_length=500)
    # can be used to give a short description about an activity taking place in a given image 
    image_caption = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class ProjectExpenses(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    exp_type = models.CharField(max_length=200)
    amount = models.IntegerField()
    comment = models.TextField(max_length=400)
    date_spent = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class ProjectEarnings(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount_earned = models.IntegerField() 
    date_earned = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class ProjectPlant(models.Model):
    plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE) 
    no = models.IntegerField()


class ProjectAnimal(models.Model):
    animal_id = models.ForeignKey(Animal, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE) 
    no = models.IntegerField()