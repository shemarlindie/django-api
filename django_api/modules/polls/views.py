from django.db.models import F, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions'

    def get_queryset(self):
        now = timezone.now()
        return (
            Question.objects
            .annotate(choice_count=Count('choice'))
            .filter(pub_date__lte=now, choice_count__gt=0)  # ignore future and without choices
            .order_by('-pub_date')
        )


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return self.model.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        return self.model.objects.filter(pub_date__lte=timezone.now())


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
