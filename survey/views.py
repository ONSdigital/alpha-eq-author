from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse
from .models import Survey
from .forms import SurveyForm


class SurveyList(ListView):
    model = Survey


class SurveyCreate(CreateView):
    model = Survey
    form_class = SurveyForm

    def get_success_url(self):
        return reverse("survey:index")