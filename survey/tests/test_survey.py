from django.core.urlresolvers import reverse
from django.test import TestCase
from survey.models import Survey, Questionnaire
from . import create_surveys, create_questionnaires, login


class SurveyTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = login(user="survey-user", email="survey-user@example.com", password="password")

    def setUp(self):
        create_surveys()
        create_questionnaires()

    def test_survey(self):
        survey1 = Survey.objects.get(survey_id="1")
        survey2 = Survey.objects.get(survey_id="2")
        self.assertEqual("Test Survey 1", survey1.title)
        self.assertEqual("Test Survey 2", survey2.title)

    def test_check_survey_count(self):
        response = SurveyTestCase.client.get(reverse('survey:index'), follow=True)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_add_survey(self):
        # first see how many surveys exist (2 are added in the setup method)
        response = SurveyTestCase.client.get(reverse('survey:index'))
        self.assertEqual(len(response.context['object_list']), 2)

        # now add a new survey
        response = SurveyTestCase.client.post(reverse('survey:create'), {'survey_list': '024'}, follow=True)
        self.assertEqual(200, response.status_code)

        # double check by sending a request to the main survey page again
        response = SurveyTestCase.client.get(reverse('survey:index'))
        self.assertEqual(len(response.context['object_list']), 3)

    def test_add_survey_fails(self):
        # first see how many surveys exist
        response = SurveyTestCase.client.get(reverse('survey:index'))
        self.assertEqual(len(response.context['object_list']), 2)

        # attempt to add an invalid survey
        response = SurveyTestCase.client.post(reverse('survey:create'), {'survey_list': '9999'}, follow=True)
        self.assertContains(response, "Select a valid choice. 9999 is not one of the available choices")

    def test_add_survey_fails_if_already_added(self):

        # first see how many surveys exist
        response = SurveyTestCase.client.get(reverse('survey:index'))
        self.assertEqual(len(response.context['object_list']), 2)

        # now add a new survey
        response = SurveyTestCase.client.post(reverse('survey:create'), {'survey_list': '024'}, follow=True)
        self.assertEqual(200, response.status_code)

        # now attempt to add the same survey
        response = SurveyTestCase.client.post(reverse('survey:create'), {'survey_list': '024'}, follow=True)

        # check we got an error message
        self.assertContains(response, "Survey has already been added")

        # check we've still got 3
        response = SurveyTestCase.client.get(reverse('survey:index'))
        self.assertEqual(len(response.context['object_list']), 3)


