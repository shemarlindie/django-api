from rest_framework import serializers

from .models import Project, Skill
from ...utils.serializers import BaseModelSerializer


class SkillSerializer(BaseModelSerializer):
    project_count = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = '__all__'

    def get_project_count(self, instance):
        return instance.projects.filter(visible=True).count()


class ProjectSerializer(BaseModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    skills_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Project.objects.all(), source='skills'
    )
    skill_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_skill_count(self, instance):
        return instance.skills.filter(visible=True).count()
