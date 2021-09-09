from django.db import models

from django_api.utils.models import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=100)
    link = models.TextField(max_length=500, null=True)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Skill(BaseModel):
    name = models.CharField(max_length=100, null=False)
    projects = models.ManyToManyField(Project, related_name='skills')

    def __str__(self):
        return self.name