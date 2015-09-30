from django.core.urlresolvers import reverse
from django.test import TestCase
from survey.models import Questionnaire, Question
from . import create_surveys, create_questionnaires, login


class QuestionTestCase(TestCase):

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

    def test_question(self):
        index = 1
        for question in Question.objects.order_by('title').all():
            self.assertEqual("Test Question %d" % index, question.title)
            if index < 4:
                self.assertEqual(Questionnaire.objects.get(questionnaire_id='1'), question.questionnaire)
            else:
                self.assertEqual(Questionnaire.objects.get(questionnaire_id='2'), question.questionnaire)
            self.assertEqual("question description %d" % index, question.description)
            self.assertEqual("question help text %d" % index, question.help_text)
            index += 1

    def test_check_question_count(self):
        response = QuestionTestCase.client.get(reverse('survey:index'))

        # check that survey one has a single questionnaire with id 1
        survey = response.context['object_list'][0]
        questionnaire_set = survey.questionnaire_set.all()
        self.assertEqual(Questionnaire.objects.get(questionnaire_id='1'), questionnaire_set[0])

        # now check that questionnaire 1 has three questions
        question_set = questionnaire_set[0].question_set.all()
        self.assertEqual(len(question_set), 3)

        # check that survey two has a single questionnaire with id 2
        survey = response.context['object_list'][1]
        questionnaire_set = survey.questionnaire_set.all()
        self.assertEqual(Questionnaire.objects.get(questionnaire_id='2'), questionnaire_set[0])

        question_set = questionnaire_set[0].question_set.all()
        self.assertEqual(len(question_set), 2)

    def test_add_question(self):
        questionnaire2 = Questionnaire.objects.get(questionnaire_id=2)
        # add a new question to questionnaire 2
        response = QuestionTestCase.client.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire2.id}), {'question_set-INITIAL_FORMS': '0', 'question_set-TOTAL_FORMS': '1', 'question_set-MIN_NUM_FORMS' : '0', 'question_set-MAX_NUM_FORMS': '1000', 'question_set-0-title': 'Test Question 6', 'question_set-0-description': 'question description 6', 'question_set-0-help_text': 'question help text 6', 'question_set-0-id': '', 'question_set-0-questionnaire': questionnaire2.id}, follow=True)
        self.assertContains(response, 'This successfully updated')
        self.assertEqual(200, response.status_code)
        # now check that questionnaire 2 has 3 questions
        response = QuestionTestCase.client.get(reverse("survey:questionnaire-summary", kwargs={'slug': '2'}))
        questionnaire = response.context['object']
        self.assertEqual(Questionnaire.objects.get(questionnaire_id="2"), questionnaire)
        question_set = questionnaire.question_set.all()
        self.assertEqual(len(question_set), 3)

    def test_add_question_fails_with_missing_title(self):
        questionnaire2 = Questionnaire.objects.get(questionnaire_id=2)
        response = QuestionTestCase.client.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire2.id}), {'question_set-INITIAL_FORMS': '0', 'question_set-TOTAL_FORMS': '1', 'question_set-MIN_NUM_FORMS' : '0', 'question_set-MAX_NUM_FORMS': '1000', 'question_set-0-title': '', 'question_set-0-description': 'question description 6', 'question_set-0-help_text': 'question help text 6', 'question_set-0-id': '', 'question_set-0-questionnaire': questionnaire2.id}, follow=True)
        self.assertContains(response, "This field is required")

    def test_add_question_fails_with_missing_description(self):
        questionnaire2 = Questionnaire.objects.get(questionnaire_id=2)
        response = QuestionTestCase.client.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire2.id}), {'question_set-INITIAL_FORMS': '0', 'question_set-TOTAL_FORMS': '1', 'question_set-MIN_NUM_FORMS' : '0', 'question_set-MAX_NUM_FORMS': '1000', 'question_set-0-title': '', 'question_set-0-description': 'question description 6', '': 'question help text 6', 'question_set-0-id': '', 'question_set-0-questionnaire': questionnaire2.id}, follow=True)
        self.assertContains(response, "This field is required")

    def test_add_question_fails_with_missing_help_text(self):
        questionnaire2 = Questionnaire.objects.get(questionnaire_id=2)
        response = QuestionTestCase.client.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire2.id}), {'question_set-INITIAL_FORMS': '0', 'question_set-TOTAL_FORMS': '1', 'question_set-MIN_NUM_FORMS' : '0', 'question_set-MAX_NUM_FORMS': '1000', 'question_set-0-title': '', 'question_set-0-description': 'question description 6', 'question_set-0-help_text': '', 'question_set-0-id': '', 'question_set-0-questionnaire': questionnaire2.id}, follow=True)
        self.assertContains(response, "This field is required")
