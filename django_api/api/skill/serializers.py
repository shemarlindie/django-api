from rest_framework import serializers

from .models import Project, Skill
from ...utils.serializers import BaseModelSerializer


class ProjectSerializer(BaseModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class SkillSerializer(BaseModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    projects_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Project.objects.all(), source='projects'
    )
    project_count = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = '__all__'

    def get_project_count(self, instance):
        return instance.projects.count()
