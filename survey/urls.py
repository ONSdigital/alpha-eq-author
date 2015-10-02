from django.conf.urls import url
from .views import SurveyList, SurveyCreate, QuestionnaireCreate, QuestionnaireReview, QuestionnairePublish
from .views import QuestionnaireDetail, QuestionnaireAPIDetail, QuestionnaireBuilder

urlpatterns = [

    url(r'^api/questionnaire/(?P<slug>[-\w]+)/$', QuestionnaireAPIDetail.as_view(), name='questionnaire-api'),
    url(r'^add/$', SurveyCreate.as_view(), name='create'),
    url(r'^questionnaire/new/(?P<survey_slug>[-\w]+)/$', QuestionnaireCreate.as_view(), name='create-questionnaire'),
    url(r'^questionnaire/(?P<slug>[-\w]+)/$', QuestionnaireDetail.as_view(), name='questionnaire-summary'),
    url(r'^questionnaire-builder/(?P<pk>[-\d]+)/$', QuestionnaireBuilder.as_view(), name='questionnaire-builder'),
    url(r'^questionnaire/(?P<slug>[-\w]+)/review', QuestionnaireReview.as_view(), name='review-questionnaire'),
    url(r'^questionnaire/(?P<slug>[-\w]+)/publish', QuestionnairePublish.as_view(), name='publish-questionnaire'),
    url(r'$', SurveyList.as_view(), name='index'),
]
