from rest_framework import viewsets

from .models import Project, Tag, IssueStatus, IssuePriority, IssueType, IssueComment, Issue
from .serializers import ProjectSerializer, IssueSerializer, TagSerializer, IssueStatusSerializer, \
    IssuePrioritySerializer, IssueTypeSerializer, IssueCommentSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('-id')
    serializer_class = TagSerializer


class IssueStatusViewSet(viewsets.ModelViewSet):
    queryset = IssueStatus.objects.all().order_by('id')
    serializer_class = IssueStatusSerializer


class IssuePriorityViewSet(viewsets.ModelViewSet):
    queryset = IssuePriority.objects.all().order_by('id')
    serializer_class = IssuePrioritySerializer


class IssueTypeViewSet(viewsets.ModelViewSet):
    queryset = IssueType.objects.all().order_by('id')
    serializer_class = IssueTypeSerializer


class IssueCommentViewSet(viewsets.ModelViewSet):
    queryset = IssueComment.objects.all().order_by('-id')
    serializer_class = IssueCommentSerializer
    filterset_fields = [f.name for f in IssueComment._meta.get_fields()]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ProjectSerializer
    search_fields = ['name', 'client', 'description']


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by('-id')
    serializer_class = IssueSerializer
    filterset_fields = [f.name for f in Issue._meta.get_fields()]
    ordering_fields = filterset_fields
    search_fields = ['name', 'description']
