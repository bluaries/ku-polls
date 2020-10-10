from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages


from .models import Question, Choice


class IndexView(generic.ListView):
    """Show a list of available polls question in index."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """Show detail of available polls question."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """ Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Show results of each polls question."""

    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Count vote in polls app."""
    question = get_object_or_404(Question, pk=question_id)

    try:
        select_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        select_choice.votes += 1
        select_choice.save()

    return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))


def vote_allowed(request, pk):
    """Check voting allowed for a question."""
    question = Question.objects.get(pk=pk)
    if not question.can_vote():
        messages.error(request, f'{"Voting is not allowed"}')
        return redirect('polls:index')
    messages.success(request, "Your choice successfully recorded. Thank you.")
    return render(request, "polls/detail.html", {"question": question})
    return redirect('polls:results')
