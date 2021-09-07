from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Project, Issue, Tag, IssueStatus, IssuePriority, IssueType, IssueComment
from ..auth.serializers import UserSerializer
from ...utils.serializers import BaseModelSerializer


class TagSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IssueStatusSerializer(BaseModelSerializer):
    class Meta:
        model = IssueStatus
        fields = '__all__'


class IssuePrioritySerializer(BaseModelSerializer):
    class Meta:
        model = IssuePriority
        fields = '__all__'


class IssueTypeSerializer(BaseModelSerializer):
    class Meta:
        model = IssueType
        fields = '__all__'


class ProjectSerializer(BaseModelSerializer):
    collaborators = UserSerializer(many=True, read_only=True)
    collaborators_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), source='collaborators'
    )
    issue_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user

        return super(ProjectSerializer, self).create(validated_data)

    def get_issue_count(self, instance):
        return instance.issues.count()


class IssueSerializer(BaseModelSerializer):
    type = IssueTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(queryset=IssueType.objects.all(), source='type')

    status = IssueStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(queryset=IssueStatus.objects.all(), source='status')

    priority = IssuePrioritySerializer(read_only=True)
    priority_id = serializers.PrimaryKeyRelatedField(queryset=IssuePriority.objects.all(), source='priority')

    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project')

    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), source='tags')

    testers = UserSerializer(many=True, read_only=True)
    testers_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), source='testers')

    fixers = UserSerializer(many=True, read_only=True)
    fixers_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), source='fixers')

    reported_by = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['reported_by'] = user

        return super(IssueSerializer, self).create(validated_data)


class IssueCommentSerializer(BaseModelSerializer):
    commenter = UserSerializer(read_only=True)

    status = IssueStatusSerializer(read_only=True, required=False, allow_null=True)
    status_id = serializers.PrimaryKeyRelatedField(queryset=IssueStatus.objects.all(), source='status', required=False, allow_null=True)

    class Meta:
        model = IssueComment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['commenter'] = user

        return super(IssueCommentSerializer, self).create(validated_data)