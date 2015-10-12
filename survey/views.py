import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, View, TemplateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from extra_views import InlineFormSetView
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect
from .models import Survey, Questionnaire, Question
from django.http import JsonResponse, Http404, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


from .forms import SurveyForm, QuestionnaireForm

from author.views import LoginRequiredMixin


class SurveyList(LoginRequiredMixin, ListView):
    model = Survey

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SurveyList, self).get_context_data(**kwargs)
        context['survey_runner_url'] = settings.SURVEY_RUNNER_URL
        return context


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
        rtn_obj['title'] = context['object'].survey.title
        rtn_obj['questionnaire_id'] = context['object'].questionnaire_id
        rtn_obj['questionnaire_title'] = context['object'].title
        rtn_obj['overview'] = context['object'].overview
        rtn_obj['questions'] = []
        for question in context['object'].question_set.all().order_by('id'):
            quest_obj = {'title':question.title,
                         'description':question.description,
                         'help_text': question.help_text}
            rtn_obj['questions'].append(quest_obj)
        return rtn_obj

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context), **response_kwargs)


class QuestionnaireCreate(LoginRequiredMixin, CreateView):
    model = Questionnaire
    form_class = QuestionnaireForm

    def render_to_response(self, context, **response_kwargs):
        survey = Survey.objects.get(survey_id=self.kwargs['survey_slug'])
        context['survey'] = survey
        return super(QuestionnaireCreate, self).render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        survey = Survey.objects.get(survey_id=self.kwargs['survey_slug'])
        form.instance.survey = survey
        return super(QuestionnaireCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse("survey:index")


class QuestionList(LoginRequiredMixin, ListView):
    model = Question

class QuestionnaireReview(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        questionnaire = Questionnaire.objects.get(questionnaire_id=self.kwargs['slug'])
        if questionnaire is not None:
            if not questionnaire.reviewed:
                questionnaire.reviewed = True
                questionnaire.save()
            return redirect(self.request.META['HTTP_REFERER'])

        raise Http404


class QuestionnairePublish(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(questionnaire_id=self.kwargs['slug'])

        if questionnaire is None:
            raise Http404

        if questionnaire.reviewed:
            questionnaire.published = True
            questionnaire.save()

            return redirect(self.request.META['HTTP_REFERER'])


class QuestionnaireBuilder(LoginRequiredMixin, TemplateView):
    template_name = 'survey/questionnaire_builder.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionnaireBuilder, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            questionnaire = Questionnaire.objects.get(id=self.kwargs['pk'])
            questionnaire.questionnaire_json = json.loads(request.body)
            questionnaire.save()
            return JsonResponse({'success':'Yippee!'})

        return JsonResponse({'error':'Nope!'})

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            questionnaire = Questionnaire.objects.get(id=self.kwargs['pk'])
            if questionnaire:
                return JsonResponse(questionnaire.questionnaire_json);
            else:
                return JsonResponse({})
        else:
            return super(QuestionnaireBuilder, self).get(request, *args, **kwargs)


