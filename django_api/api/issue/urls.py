from django.urls import path, include
from rest_framework import routers

from .views import TagViewSet, IssuePriorityViewSet, IssueStatusViewSet, IssueTypeViewSet, IssueCommentViewSet, \
    ProjectViewSet, IssueViewSet

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'issue-statuses', IssueStatusViewSet)
router.register(r'issue-priorities', IssuePriorityViewSet)
router.register(r'issue-types', IssueTypeViewSet)
router.register(r'comments', IssueCommentViewSet)

app_name = 'issue_api'

urlpatterns = [
    path('', include(router.urls)),
]
