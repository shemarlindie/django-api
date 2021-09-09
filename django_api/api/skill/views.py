from rest_framework import viewsets

from .models import Project, Skill
from .serializers import ProjectSerializer, SkillSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ProjectSerializer
    filterset_fields = [f.name for f in Project._meta.get_fields()]
    ordering_fields = filterset_fields
    search_fields = ['name', 'description']


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('id')
    serializer_class = SkillSerializer
    filterset_fields = [f.name for f in Skill._meta.get_fields()]
    ordering_fields = filterset_fields
    search_fields = ['name']
