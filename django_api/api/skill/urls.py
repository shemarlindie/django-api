from django.urls import path, include
from rest_framework import routers

from .views import ProjectViewSet, SkillViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'skills', SkillViewSet)

app_name = 'skill_api'

urlpatterns = [
    path('', include(router.urls)),
]
