import json
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, View, TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .models import Survey, Questionnaire
from django.http import JsonResponse, Http404, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


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
        for question in context['object'].questionnaire_json:
            if 'dndType' in question.keys():
                del question['dndType']
            if 'type' in question.keys():
                del question['type']
            rtn_obj['questions'].append(question)
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
            if questionnaire.published:
                return JsonResponse({'error': 'Already Published!'})

            json_data = json.loads(request.body);
            if questionnaire.is_locked(request.user.username):
                return JsonResponse({'error': 'Locked for editing!', 'locked': questionnaire.locked_by})
            else:
                if 'unlock' in json_data:
                    questionnaire.unlock()
                    return JsonResponse({'success': 'Unlocked'})
                else:
                   question_meta = json_data['meta']
                   questionnaire.title = question_meta['title']
                   questionnaire.overview = question_meta['overview']
                   questionnaire.last_used_id = question_meta['last_used_id']
                   questionnaire.questionnaire_json = json_data['questionList']
                   questionnaire.reviewed = False
                   questionnaire.lock(request.user.username)
                   questionnaire.save()
                   return JsonResponse({'success': 'Your questionnaire has been saved!'})
        return JsonResponse({'error': 'Your questionnaire could not be saved!'})




    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            questionnaire = Questionnaire.objects.get(id=self.kwargs['pk'])
            if questionnaire:
                if questionnaire.is_locked(request.user.username):
                    return JsonResponse({'error': 'Locked for editing!', 'locked': questionnaire.locked_by})
                else:
                    questionnaire.lock(request.user.username)
                    questionList = questionnaire.questionnaire_json
                if not questionList:
                    questionList = []

                jsonResponse = {
                    'meta': {
                        'title': questionnaire.title,
                        'overview': questionnaire.overview,
                        'questionnaire_id' : questionnaire.questionnaire_id,
                        'last_used_id': questionnaire.last_used_id
                    },
                    'questionList' : questionList
                }

                return JsonResponse(jsonResponse);
            else:
                return JsonResponse({})
        else:
            return super(QuestionnaireBuilder, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuestionnaireBuilder, self).get_context_data(**kwargs)

        context['questionnaire'] = Questionnaire.objects.get(id=self.kwargs['pk'])

        return context
