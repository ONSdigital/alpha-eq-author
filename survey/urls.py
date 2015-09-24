from django.conf.urls import url
from .views import SurveyList, SurveyCreate, QuestionnaireCreate, QuestionCreate, QuestionnaireDetail

urlpatterns = [
    url(r'add/$', SurveyCreate.as_view(), name='create'),
    url(r'questionnaire/new/(.*)/$', QuestionnaireCreate.as_view(), name='create-questionnaire'),
    url(r'questionnaire/(?P<slug>[-\w]+)/$', QuestionnaireDetail.as_view(), name='questionnaire-summary'),
    url(r'question/(?P<questionnaire_slug>[-\w]+)$', QuestionCreate.as_view(), name='create-question'),
    url(r'$', SurveyList.as_view(), name='index'),
]