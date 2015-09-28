from django.core.urlresolvers import reverse
from django.test import TestCase
from survey.models import Survey, Questionnaire
from . import create_surveys, create_questionnaires, login


class QuestionnaireTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = login(user="questionnaire-user", email="questionnaire-user@example.com", password="password")

    def setUp(self):
        create_surveys()
        create_questionnaires()

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
        response = QuestionnaireTestCase.client.get(reverse('survey:index'))
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
        # add a new questionnaire to survey 1
        response = QuestionnaireTestCase.client.post(reverse("survey:create-questionnaire", kwargs={'survey_slug': '1'}), {'title' : 'Test Questionnaire 3', 'questionnaire_id': '3', 'overview': 'questionnaire overview 3'}, follow=True)
        self.assertEqual(200, response.status_code)

        # now check that survey 1 has two questionnaires
        response = QuestionnaireTestCase.client.get(reverse('survey:index'))
        survey = response.context['object_list'][0]
        self.assertEqual(Survey.objects.get(survey_id='1'), survey)
        questionnaire_set = survey.questionnaire_set.all()
        self.assertEqual(len(questionnaire_set), 2)
        self.assertEqual(Questionnaire.objects.get(questionnaire_id='3'), questionnaire_set[0])
        self.assertEqual(Questionnaire.objects.get(questionnaire_id='1'), questionnaire_set[1])

    def test_add_questionnaire_fails_when_overview_is_missing(self):
        # attempt to add an invalid questionnaire (i.e. missing the overview field)
        response = QuestionnaireTestCase.client.post(reverse("survey:create-questionnaire", kwargs={'survey_slug': '1'}), {'title': 'Test Questionnaire 4', 'questionnaire_id': '4'}, follow=True)
        self.assertContains(response, "This field is required")

    def test_add_questionnaire_fails_when_title_is_missing(self):
        # attempt to add an invalid questionnaire (i.e. missing the overview field)
        response = QuestionnaireTestCase.client.post(reverse("survey:create-questionnaire", kwargs={'survey_slug': '1'}), {'questionnaire_id': '4', 'overview': 'questionnaire overview 4'}, follow=True)
        self.assertContains(response, "This field is required")

    def test_add_questionnaire_fails_when_id_is_missing(self):
        # attempt to add an invalid questionnaire (i.e. missing the overview field)
        response = QuestionnaireTestCase.client.post(reverse("survey:create-questionnaire", kwargs={'survey_slug': '1'}), {'title': 'Test Questionnaire 4', 'overview': 'questionnaire overview 4'}, follow=True)
        self.assertContains(response, "This field is required")
