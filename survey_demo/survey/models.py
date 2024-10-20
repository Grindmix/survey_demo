from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse

import uuid

class Survey(models.Model):
    
    def __str__(self):
        return self.title
    
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Дата публикации')
    require_login = models.BooleanField(default=True)

    def questions(self):
        if self.pk:
            return Question.objects.filter(survey=self.pk)
        else:
            return None

    def get_absolute_url(self):
        return reverse("survey-form", args=[str(self.id)])
    

class Question(models.Model):
    
    def __str__(self):
        return self.question_text

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    CHOICE_TYPE = (
        ('t', 'Text'),
        ('r', 'Radio'),
        ('c', 'Checkbox'),
    )

    choice_type = models.CharField(max_length=1, choices=CHOICE_TYPE, default='r', help_text='Вид ответов на вопрос')

    def choices(self):
        if self.pk:
            chocies = [(c['id'], c['choice']) for c in Choice.objects.filter(question=self.pk).values('id','choice')]
            return chocies
        else:
            return None


class SurveyResult(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique id of Survey result")
    user = models.CharField(max_length=200, null=True, blank=True)
    survey = models.ForeignKey(Survey, on_delete=CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Choice(models.Model):
    
    def __str__(self):
        return self.choice

    question = models.ForeignKey(Question, on_delete=CASCADE)    
    choice = models.CharField(max_length=200)


class ResultChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=CASCADE)
    choice_result = models.TextField(null=True, blank=True)
    refer_survey_result = models.ForeignKey(SurveyResult, on_delete=CASCADE)