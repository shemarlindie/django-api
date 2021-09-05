from rest_framework import viewsets

from .serializers import QuestionSerializer, ChoiceSerializer
from django_api.modules.polls.models import Question, Choice


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for question manipulation.
    """
    queryset = Question.objects.all().order_by('-id')
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for question manipulation.
    """
    queryset = Choice.objects.all().order_by('-id')
    serializer_class = ChoiceSerializer
