from django import forms

from survey.models import Question, SurveyResult, ResultChoice

class SurveyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        survey = kwargs.pop('survey')
        self.survey = survey
        username = kwargs.pop('username')
        self.username = username 
        super(SurveyForm, self).__init__(*args, **kwargs)
        
        for q in survey.questions():
            if q.choice_type == 't':
                self.fields["question_%d" % q.pk] = forms.CharField(label=q.question_text, widget=forms.TextInput)
            elif q.choice_type == 'r':
                choices = q.choices()
                self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.question_text, widget=forms.RadioSelect, choices=choices)
            elif q.choice_type == 'c':
                choices = q.choices()
                self.fields["question_%d" % q.pk] = forms.MultipleChoiceField(label=q.question_text, widget=forms.CheckboxSelectMultiple, choices=choices)

    def save_results(self):
        refer_survey_result = SurveyResult(survey=self.survey)
        if self.username != None:
            refer_survey_result.user = self.username
        refer_survey_result.save()
        question_list = Question.objects.filter(survey=self.survey)
        i = 0
        for field_name, field_value in self.cleaned_data.items():
            if field_name.startswith("question_"):
                q = question_list[i]
                choice = ResultChoice(question=q, choice_result=field_value, refer_survey_result=refer_survey_result)
                choice.save()
                i += 1

        return refer_survey_result