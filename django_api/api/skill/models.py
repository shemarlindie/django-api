from django.db import models

from django_api.utils.models import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=500)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Skill(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    projects = models.ManyToManyField(Project, related_name='skills')
    visible = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name