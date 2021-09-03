from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.all().order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, model_id):
    question = get_object_or_404(Question, pk=model_id)
    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
    except (Choice.DoesNotExist, KeyError):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice.',
        })
    else:
        choice.votes = F('votes') + 1
        choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
