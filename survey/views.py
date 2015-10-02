from django.views.generic import ListView, CreateView, DetailView, View
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .models import Survey, Questionnaire, Question
from django.http import JsonResponse, Http404
from django.conf import settings

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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(QuestionnaireDetail, self).get_context_data(**kwargs)
        context['survey_runner_url'] = settings.SURVEY_RUNNER_URL
        return context


class QuestionnaireAPIDetail(DetailView):
    model = Questionnaire
    slug_field = 'id'

    def get_data(self, context):
        rtn_obj = {}
        rtn_obj['questionnaire_title'] = context['object'].title
        rtn_obj['overview'] = context['object'].overview
        rtn_obj['questions'] = []
        for question in context['object'].question_set.all():
            quest_obj = {'title':question.title,
                         'help_text': question.help_text,
                         'error_text': question.error_text}
            rtn_obj['questions'].append(quest_obj)
        return rtn_obj

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context), **response_kwargs)


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

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        questionnaire = Questionnaire.objects.get(questionnaire_id=self.kwargs['questionnaire_slug'])
        if questionnaire.published:
            return self.form_invalid(self, form)

        return super(QuestionCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        questionnaire = Questionnaire.objects.get(questionnaire_id=self.kwargs['questionnaire_slug'])
        form.instance.questionnaire = questionnaire
        result = super(QuestionCreate, self).form_valid(form)
        if result:
            questionnaire.reviewed = False
            questionnaire.save()
        return result

    def get_success_url(self):
        return reverse("survey:questionnaire-summary", kwargs={'slug': self.kwargs['questionnaire_slug']})


class QuestionnaireReview(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        questionnaire = Questionnaire.objects.get(questionnaire_id=self.kwargs['slug'])
        if questionnaire is not None:
            if not questionnaire.reviewed:
                questionnaire.reviewed = True
                questionnaire.save()
            return redirect(reverse("survey:questionnaire-summary", kwargs={'slug': self.kwargs['slug']}))

        raise Http404


class QuestionnairePublish(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(questionnaire_id=self.kwargs['slug'])

        if questionnaire is None:
            raise Http404

        if questionnaire.reviewed:
            questionnaire.published = True
            questionnaire.save()

            return redirect(reverse("survey:questionnaire-summary", kwargs={'slug': self.kwargs['slug']}))

