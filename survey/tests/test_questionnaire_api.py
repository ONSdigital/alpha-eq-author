from django.core.urlresolvers import reverse
from django.test import TestCase
from survey.models import Questionnaire, Question
from . import create_surveys, create_questionnaires, login


class QuestionnaireAPITestCase(TestCase):

        @classmethod
        def setUpTestData(cls):
            cls.client = login(user="question-user", email="question-user@example.com", password="password")

        def setUp(self):
            create_surveys()
            create_questionnaires()
            # first questionnaire has three questions
            Question.objects.create(title="Test Question 1", questionnaire=Questionnaire.objects.get(questionnaire_id='1'), description='question description 1', help_text='question help text 1')
            Question.objects.create(title="Test Question 2", questionnaire=Questionnaire.objects.get(questionnaire_id='1'), description='question description 2', help_text='question help text 2')
            Question.objects.create(title="Test Question 3", questionnaire=Questionnaire.objects.get(questionnaire_id='1'), description='question description 3', help_text='question help text 3')

            # whilst the second questionnaire has two questions
            Question.objects.create(title="Test Question 4", questionnaire=Questionnaire.objects.get(questionnaire_id='2'), description='question description 4', help_text='question help text 4')
            Question.objects.create(title="Test Question 5", questionnaire=Questionnaire.objects.get(questionnaire_id='2'), description='question description 5', help_text='question help text 5')

        def test_render_to_json_object_matches_schema(self):
            ques_1 = Questionnaire.objects.get(questionnaire_id='1')
            response = QuestionnaireAPITestCase.client.get(reverse("survey:questionnaire-api", kwargs={'slug': ques_1.pk}), follow=True)

            self.assertEqual(200, response.status_code)
            import json
            questionnaire = json.loads(response.content)
            self.assertEqual(3, len(questionnaire['questions']))

        def test_questionnaire_ordering_correct(self):
            ques_1 = Questionnaire.objects.get(questionnaire_id='1')
            response = QuestionnaireAPITestCase.client.get(reverse("survey:questionnaire-api", kwargs={'slug': ques_1.pk}), follow=True)

            self.assertEqual(200, response.status_code)
            import json
            questionnaire = json.loads(response.content)
            self.assertEqual('Test Question 1', questionnaire['questions'][0]['title'])
            self.assertEqual('Test Question 2', questionnaire['questions'][1]['title'])
            self.assertEqual('Test Question 3', questionnaire['questions'][2]['title'])