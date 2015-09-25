from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponse
from .models import Survey, Questionnaire
from .forms import SurveyForm
from author.views import LoginRequiredMixin


class SurveyList(LoginRequiredMixin, ListView):
    model = Survey


class SurveyCreate(LoginRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyForm

    def get_success_url(self):
        return reverse("survey:index")


class QuestionnaireCreate(LoginRequiredMixin, CreateView):
    model = Questionnaire
    fields = ['title', 'questionnaire_id', 'overview']

    def form_valid(self, form):
        survey = Survey.objects.get(survey_id=self.args[0])
        form.instance.survey = survey
        return super(QuestionnaireCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse("survey:index")
