from django.contrib import admin
from django.db import models
from django.db.models import fields

from .models import Survey, Question, Choice, SurveyResult


class QuestionInLine(admin.TabularInline):
    model = Question
    exclude = ('choices',)
    extra = 0

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'require_login')
    fields = ['title', 'pub_date', 'require_login']
    inlines = [QuestionInLine]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'survey')
    search_fields = ['survey__title']
    inlines = [ChoiceInLine]

admin.site.register(SurveyResult)
