from django.test import Client
from author.tests import create_user
from survey.models import Survey, Questionnaire


def create_surveys():
    Survey.objects.create(title="Test Survey 1", survey_id="1")
    Survey.objects.create(title="Test Survey 2", survey_id="2")


def login(user, email, password):
    user = create_user(username=user, email=email, password=password)
    client = Client()
    client.login(username=user.username, password=password)
    return client


def create_questionnaires():
    Questionnaire.objects.create(title="Test Questionnaire 1", survey=Survey.objects.get(survey_id='1'), questionnaire_id="1", overview='questionnaire overview 1')
    Questionnaire.objects.create(title="Test Questionnaire 2", survey=Survey.objects.get(survey_id='2'), questionnaire_id="2", overview='questionnaire overview 2')