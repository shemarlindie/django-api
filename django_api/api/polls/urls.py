from django.urls import path, include
from rest_framework import routers

from .views import QuestionViewSet, ChoiceViewSet

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)

app_name = 'polls_api'

urlpatterns = [
    path('', include(router.urls)),
]
