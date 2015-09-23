from django.test import TestCase, Client
from .models import Survey, Questionnaire


def create_surveys():
    Survey.objects.create(title="Test Survey 1", survey_id="1")
    Survey.objects.create(title="Test Survey 2", survey_id="2")


class SurveyTestCase(TestCase):

    def setUp(self):
        create_surveys()

    def test_survey(self):
        survey1 = Survey.objects.get(survey_id="1")
        survey2 = Survey.objects.get(survey_id="2")
        self.assertEqual("Test Survey 1", survey1.title)
        self.assertEqual("Test Survey 2", survey2.title)

    def test_check_survey_count(self):
        client = Client()
        response = client.get('/surveys/')
        self.assertEqual(len(response.context['object_list']), 2)

    def test_add_survey(self):
        client = Client()

        # first see how many surveys exist (2 are added in the setup method)
        response = client.get('/surveys/')
        self.assertEqual(len(response.context['object_list']), 2)

        # now add a new survey
        response = client.post('/surveys/add/', {'survey_list': '024'}, follow=True)
        self.assertEqual(200, response.status_code)
        # check we've got an additional survey
        self.assertEqual(len(response.context['object_list']), 3)

        # double check by sending a request to the main survey page again
        response = client.get('/surveys/')
        self.assertEqual(len(response.context['object_list']), 3)

    def test_add_survey_fails(self):
        client = Client()

        # first see how many surveys exist
        response = client.get('/surveys/')
        self.assertEqual(len(response.context['object_list']), 2)

        # attempt to add an invalid survey
        response = client.post('/surveys/add/', {'survey_list': '9999'}, follow=True)
        self.assertContains(response, "Select a valid choice. 9999 is not one of the available choices")


class QuestionnaireTestCase(TestCase):

    def setUp(self):
        create_surveys()
        Questionnaire.objects.create(title="Test Questionnaire 1", survey=Survey.objects.get(survey_id='1'), questionnaire_id="1", overview='questionnaire overview 1')
        Questionnaire.objects.create(title="Test Questionnaire 2", survey=Survey.objects.get(survey_id='2'), questionnaire_id="2", overview='questionnaire overview 2')

    def test_questionnaire(self):
        questionnaire1 = Questionnaire.objects.get(questionnaire_id='1')
        questionnaire2 = Questionnaire.objects.get(questionnaire_id='2')
        self.assertEqual("Test Questionnaire 1", questionnaire1.title)
        self.assertEqual("Test Questionnaire 2", questionnaire2.title)
        self.assertEqual("questionnaire overview 1", questionnaire1.overview)
        self.assertEqual("questionnaire overview 2", questionnaire2.overview)
        self.assertEqual(Survey.objects.get(survey_id='1'), questionnaire1.survey)
        self.assertEqual(Survey.objects.get(survey_id='2'), questionnaire2.survey)

    def test_check_question_count(self):
        client = Client()
        response = client.get("/surveys/")

        # check that survey one has a single questionnaire with id 1
        survey = response.context['object_list'][0]
        self.assertEqual(Survey.objects.get(survey_id='1'), survey)
        questionnaire_set = survey.questionnaire_set.all()
        self.assertEqual(len(questionnaire_set), 1)
        self.assertEqual(Questionnaire.objects.get(questionnaire_id='1'), questionnaire_set[0])

        # check that survey two has a single questionnaire with id 2
        survey = response.context['object_list'][1]
        self.assertEqual(Survey.objects.get(survey_id='2'), survey)
        questionnaire_set = survey.questionnaire_set.all()
        self.assertEqual(len(questionnaire_set), 1)
        self.assertEqual(Questionnaire.objects.get(questionnaire_id='2'), questionnaire_set[0])

    def test_add_questionnaire(self):
        client = Client()

        # add a new questionnaire to survey 1
        response = client.post("/surveys/questionnaire/1/", {'title' : 'Test Questionnaire 3', 'questionnaire_id': '3', 'overview': 'questionnaire overview 3'}, follow=True)
        self.assertEqual(200, response.status_code)

        # now check that survey 1 has two questionnaires
        response = client.get("/surveys/")
        survey = response.context['object_list'][0]
        self.assertEqual(Survey.objects.get(survey_id='1'), survey)
        questionnaire_set = survey.questionnaire_set.all()
        self.assertEqual(len(questionnaire_set), 2)
        self.assertEqual(Questionnaire.objects.get(questionnaire_id='3'), questionnaire_set[0])
        self.assertEqual(Questionnaire.objects.get(questionnaire_id='1'), questionnaire_set[1])

    def test_add_questionnaire_fails_when_overview_is_missing(self):
        client = Client()
        # attempt to add an invalid questionnaire (i.e. missing the overview field)
        response = client.post("/surveys/questionnaire/1/", {'title': 'Test Questionnaire 4', 'questionnaire_id': '4'}, follow=True)

        self.assertContains(response, "This field is required")

    def test_add_questionnaire_fails_when_title_is_missing(self):
        client = Client()
        # attempt to add an invalid questionnaire (i.e. missing the overview field)
        response = client.post("/surveys/questionnaire/1/", {'questionnaire_id': '4', 'overview': 'questionnaire overview 4'}, follow=True)

        self.assertContains(response, "This field is required")

    def test_add_questionnaire_fails_when_id_is_missing(self):
        client = Client()
        # attempt to add an invalid questionnaire (i.e. missing the overview field)
        response = client.post("/surveys/questionnaire/1/", {'title': 'Test Questionnaire 4', 'overview': 'questionnaire overview 4'}, follow=True)

        self.assertContains(response, "This field is required")