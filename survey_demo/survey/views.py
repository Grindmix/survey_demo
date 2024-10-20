from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse

from .models import Survey, SurveyResult, ResultChoice, Choice
from .forms import SurveyForm

import ast

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'survey_list'

    def get_queryset(self):
        return Survey.objects.all()


def survey_form(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    if request.method == 'POST':
        form = SurveyForm(request.POST, survey=survey, username=username)
        if form.is_valid():
            results = form.save_results()
            return HttpResponseRedirect(reverse('survey-results', args=[results.id]))
    else:
        form = SurveyForm(survey=survey, username=username)

    context = {
        'form': form,
        'survey': survey,
    }

    return render(request, 'survey_form.html', context)


def survey_results_view(request, pk):
    survey_results = get_object_or_404(SurveyResult, pk=pk)
    result_choices = ResultChoice.objects.filter(refer_survey_result=survey_results)
    choices = {}
    for c in result_choices:
        try:
            choice_result = ast.literal_eval(c.choice_result)
        except:
            choice_result = c.choice_result  

        if isinstance(choice_result, list):
            l = []
            for i in choice_result:
                object = Choice.objects.get(id=i)
                field = object._meta.get_field('choice')
                l.append(field.value_from_object(object))
            choices[c.question.id] = l
        elif isinstance(choice_result, int):
            object = Choice.objects.get(id=choice_result)
            field = object._meta.get_field('choice')
            choices[c.question.id] = field.value_from_object(object)
        elif isinstance(choice_result, str):
            choices[c.question.id] = choice_result

    context = {
        'result_choices': result_choices,
        'survey_results': survey_results,
        'choices' : choices,
    }

    return render(request, 'survey_results_page.html', context)