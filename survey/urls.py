from django.conf.urls import url
from .views import SurveyList, SurveyCreate, QuestionnaireCreate, QuestionCreate, QuestionnaireReview
from .views import QuestionnaireDetail, QuestionnaireAPIDetail

urlpatterns = [
    url(r'^api/questionnaire/(?P<slug>[-\w]+)/$', QuestionnaireAPIDetail.as_view(), name='questionnaire-api'),
    url(r'^add/$', SurveyCreate.as_view(), name='create'),
    url(r'^questionnaire/new/(?P<survey_slug>[-\w]+)/$', QuestionnaireCreate.as_view(), name='create-questionnaire'),
    url(r'^questionnaire/(?P<slug>[-\w]+)/$', QuestionnaireDetail.as_view(), name='questionnaire-summary'),
    url(r'^question/(?P<questionnaire_slug>[-\w]+)/$', QuestionCreate.as_view(), name='create-question'),
    url(r'^questionnaire/(?P<slug>[-\w]+)/review', QuestionnaireReview.as_view(), name='review-questionnaire'),
    url(r'$', SurveyList.as_view(), name='index'),
]
