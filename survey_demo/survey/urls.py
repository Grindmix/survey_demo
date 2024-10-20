from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('id=<int:pk>', views.survey_form, name='survey-form'),
    path('results/<uuid:pk>/', views.survey_results_view, name='survey-results'),
    path('accounts/', include('django.contrib.auth.urls')),
]
