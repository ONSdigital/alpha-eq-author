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
        response = client.post('/surveys/add/', {'survey_list': '024'}, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.context['object_list']), 3)


