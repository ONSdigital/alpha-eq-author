from django.conf.urls import url
from .views import SurveyList, SurveyCreate, QuestionnaireCreate

urlpatterns = [
    url(r'add/$', SurveyCreate.as_view(), name='create'),
    url(r'questionnaire/(.*)/$', QuestionnaireCreate.as_view(), name='create-questionnaire'),
    url(r'$', SurveyList.as_view(), name='index'),
]