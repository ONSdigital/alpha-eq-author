from django.test import TestCase, Client
from .models import Survey


class SurveyTestCase(TestCase):
    def setUp(self):
        Survey.objects.create(title="Test Survey 1", survey_id="1")
        Survey.objects.create(title="Test Survey 2", survey_id="2")

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
