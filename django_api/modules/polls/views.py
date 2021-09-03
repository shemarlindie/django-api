from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader
from django.urls import reverse

from .models import Question, Choice


def index(request):
    context = {'questions': Question.objects.order_by('-pub_date')}

    return render(request, 'polls/index.html', context)


def detail(request, model_id):
    question = get_object_or_404(Question, pk=model_id)

    return render(request, 'polls/detail.html', {'question': question})


def results(request, model_id):
    question = get_object_or_404(Question, pk=model_id)

    return render(request, 'polls/results.html', {'question': question})


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
