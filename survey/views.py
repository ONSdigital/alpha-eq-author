from django.views.generic import ListView, CreateView, DetailView
from django.core.urlresolvers import reverse
from .models import Survey, Questionnaire, Question
from .forms import SurveyForm, QuestionnaireForm
from author.views import LoginRequiredMixin


class SurveyList(LoginRequiredMixin, ListView):
    model = Survey


class SurveyCreate(LoginRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyForm

    def get_success_url(self):
        return reverse("survey:create-questionnaire", kwargs={'survey_slug': self.object.survey_id})


class QuestionnaireDetail(LoginRequiredMixin, DetailView):
    model = Questionnaire
    slug_field = 'questionnaire_id'


class QuestionnaireCreate(LoginRequiredMixin, CreateView):
    model = Questionnaire
    form_class = QuestionnaireForm

    def form_valid(self, form):
        survey = Survey.objects.get(survey_id=self.kwargs['survey_slug'])
        form.instance.survey = survey
        return super(QuestionnaireCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse("survey:index")


class QuestionList(LoginRequiredMixin, ListView):
    model = Question


class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'description', 'help_text', 'error_text']

    def form_valid(self, form):
        questionnaire = Questionnaire.objects.get(questionnaire_id=self.kwargs['questionnaire_slug'])
        form.instance.questionnaire = questionnaire
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse("survey:questionnaire-summary", kwargs={'slug': self.kwargs['questionnaire_slug'] })
