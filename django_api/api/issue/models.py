from django.contrib.auth.models import User
from django.db import models

from django_api.utils.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class IssueStatus(BaseModel):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class IssuePriority(BaseModel):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class IssueType(BaseModel):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Project(BaseModel):
    name = models.CharField(max_length=100, null=False)
    client = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=500, null=True)
    date_due = models.DateTimeField(
        'The date a project is expected to be completed by', null=True
    )
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='projects', editable=False)
    collaborators = models.ManyToManyField(User, related_name='collaborations', blank=True)

    def __str__(self):
        return self.name


class Issue(BaseModel):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=10000, null=False)
    date_due = models.DateTimeField(
        'The date an issue is expected to be completed by', null=True
    )
    reported_by = models.ForeignKey(User, on_delete=models.RESTRICT, editable=False)
    testers = models.ManyToManyField(User, related_name='issues_tested', blank=True)
    fixers = models.ManyToManyField(User, related_name='issues_fixed', blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.ForeignKey(IssueStatus, on_delete=models.RESTRICT)
    priority = models.ForeignKey(IssuePriority, on_delete=models.RESTRICT)
    type = models.ForeignKey(IssueType, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class IssueComment(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500)
    commenter = models.ForeignKey(User, on_delete=models.RESTRICT, editable=False)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    status = models.ForeignKey(IssueStatus, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.description
