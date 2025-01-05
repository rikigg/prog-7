from django.template import loader
from .models import Question
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render, redirect
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from .models import Choice, Question, Survey
from .forms import SurveyForm, QuestionForm, UserRegistrationForm


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


@login_required
def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save()
            return redirect('polls:edit_survey', survey_id=survey.id)
    else:
        form = SurveyForm()
    return render(request, 'polls/create_survey.html', {'form': form})


@login_required
def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.pub_date = timezone.now()
            question.save()
            return redirect('polls:edit_survey', survey_id=survey.id)
    else:
        form = QuestionForm()
    questions = survey.question_set.all().order_by('order')
    return render(request, 'polls/edit_survey.html', {
        'survey': survey,
        'form': form,
        'questions': questions
    })


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def take_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.question_set.all().order_by('order')
    return render(request, 'polls/take_survey.html', {
        'survey': survey,
        'questions': questions
    })


def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.question_set.all().order_by('order')
    return render(request, 'polls/survey_results.html', {
        'survey': survey,
        'questions': questions
    })


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'polls/register.html', {'form': form})


def search_view(request):
    return render(request, 'polls/search.html')
