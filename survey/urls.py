from django.conf.urls import url
from .views import SurveyList, SurveyCreate

urlpatterns = [
    url(r'add/$', SurveyCreate.as_view(), name='create'),
    url(r'$', SurveyList.as_view(), name='index'),
]