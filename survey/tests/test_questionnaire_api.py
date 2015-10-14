from django.core.urlresolvers import reverse
from django.test import TestCase
from survey.models import Questionnaire
from . import create_surveys, create_questionnaires, login
import json


class QuestionnaireAPITestCase(TestCase):

        @classmethod
        def setUpTestData(cls):
            cls.client = login(user="question-user", email="question-user@example.com", password="password")

        def setUp(self):
            create_surveys()
            create_questionnaires()
            questionnaire1 = Questionnaire.objects.get(questionnaire_id='1')
            questionnaire2 = Questionnaire.objects.get(questionnaire_id='2')

            # first questionnaire has three questions
            questionnaire1.questionnaire_json = json.loads('[{"questionType": "InputText", "questionHelp": "All sizes count, even grandfathers.", "questionError": "Sorry - not a valid entry.", "questionText": "Question 1?"},{"questionType": "InputText", "questionHelp": "All sizes count, even grandfathers.", "questionError": "Sorry - not a valid entry.", "questionText": "Question 2?"},{"questionType": "InputText", "questionHelp": "All sizes count, even grandfathers.", "questionError": "Sorry - not a valid entry.", "questionText": "Question 3?"}]')

            # whilst the second questionnaire has two questions
            questionnaire2.questionnaire_json = json.loads('[{"questionType": "InputText", "questionHelp": "All sizes count, even grandfathers.", "questionError": "Sorry - not a valid entry.", "questionText": "Question 1?"},{"questionType": "InputText", "questionHelp": "All sizes count, even grandfathers.", "questionError": "Sorry - not a valid entry.", "questionText": "Question 2?"}]')

            #save
            questionnaire1.save()
            questionnaire2.save()

        def test_render_to_json_object_matches_schema(self):
            ques_1 = Questionnaire.objects.get(questionnaire_id='1')
            response = QuestionnaireAPITestCase.client.get(reverse("survey:questionnaire-api", kwargs={'slug': ques_1.pk}), follow=True)

            self.assertEqual(200, response.status_code)
            questionnaire = json.loads(response.content)
            self.assertEqual(3, len(questionnaire['questions']))

        def test_questionnaire_ordering_correct(self):
            ques_1 = Questionnaire.objects.get(questionnaire_id='1')
            response = QuestionnaireAPITestCase.client.get(reverse("survey:questionnaire-api", kwargs={'slug': ques_1.pk}), follow=True)
            self.assertEqual(200, response.status_code)
            questionnaire = json.loads(response.content)
            self.assertEqual('Question 1?', questionnaire['questions'][0]['questionText'])
            self.assertEqual('Question 2?', questionnaire['questions'][1]['questionText'])
            self.assertEqual('Question 3?', questionnaire['questions'][2]['questionText'])