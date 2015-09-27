from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from author.tests import create_user
from .models import Survey, Questionnaire, Question


def create_surveys():
    Survey.objects.create(title="Test Survey 1", survey_id="1")
    Survey.objects.create(title="Test Survey 2", survey_id="2")


def login(user, email, password):
    user = create_user(username=user, email=email, password=password)
    client = Client()
    login = client.login(username=user.username, password=password)
    return client


def create_questionnaires():
    Questionnaire.objects.create(title="Test Questionnaire 1", survey=Survey.objects.get(survey_id='1'), questionnaire_id="1", overview='questionnaire overview 1')
    Questionnaire.objects.create(title="Test Questionnaire 2", survey=Survey.objects.get(survey_id='2'), questionnaire_id="2", overview='questionnaire overview 2')


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


class QuestionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = login(user="question-user", email="question-user@example.com", password="password")

    def setUp(self):
        create_surveys()
        create_questionnaires()
        # first questionnaire has three questions
        Question.objects.create(title="Test Question 1", questionnaire=Questionnaire.objects.get(questionnaire_id='1'), description='question description 1', help_text='question help text 1', error_text='question error text 1')
        Question.objects.create(title="Test Question 2", questionnaire=Questionnaire.objects.get(questionnaire_id='1'), description='question description 2', help_text='question help text 2', error_text='question error text 2')
        Question.objects.create(title="Test Question 3", questionnaire=Questionnaire.objects.get(questionnaire_id='1'), description='question description 3', help_text='question help text 3', error_text='question error text 3')

        # whilst the second questionnaire has two questions
        Question.objects.create(title="Test Question 4", questionnaire=Questionnaire.objects.get(questionnaire_id='2'), description='question description 4', help_text='question help text 4', error_text='question error text 4')
        Question.objects.create(title="Test Question 5", questionnaire=Questionnaire.objects.get(questionnaire_id='2'), description='question description 5', help_text='question help text 5', error_text='question error text 5')

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
            self.assertEqual("question error text %d" % index, question.error_text)
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
        # add a new question to questionnaire 2
        response = QuestionTestCase.client.post(reverse("survey:create-question", kwargs={'questionnaire_slug': '2'}), {'title': 'Test Question 6', 'description': 'question description 6', 'help_text': 'question help text 6', 'error_text' : 'question error text 6'}, follow=True)
        self.assertEqual(200, response.status_code)
        # now check that questionnaire 2 has 3 questions
        response = QuestionTestCase.client.get(reverse("survey:questionnaire-summary", kwargs={'slug': '2'}))
        questionnaire = response.context['object']
        self.assertEqual(Questionnaire.objects.get(questionnaire_id="2"), questionnaire)
        question_set = questionnaire.question_set.all()
        self.assertEqual(len(question_set), 3)

    def test_add_question_fails_with_missing_title(self):
        response = QuestionTestCase.client.post(reverse("survey:create-question", kwargs={'questionnaire_slug': '2'}), {'description': 'question description 6', 'help_text': 'question help text 6', 'error_text' : 'question error text 6'}, follow=True)
        self.assertContains(response, "This field is required")

    def test_add_question_fails_with_missing_description(self):
        response = QuestionTestCase.client.post(reverse("survey:create-question", kwargs={'questionnaire_slug': '2'}), {'title': 'Test Question 6', 'help_text': 'question help text 6', 'error_text' : 'question error text 6'}, follow=True)
        self.assertContains(response, "This field is required")

    def test_add_question_fails_with_missing_help_text(self):
        response = QuestionTestCase.client.post(reverse("survey:create-question", kwargs={'questionnaire_slug': '2'}), {'title': 'Test Question 6', 'description': 'question description 6', 'error_text' : 'question error text 6'}, follow=True)
        self.assertContains(response, "This field is required")

    def test_add_question_fails_with_missing_error_text(self):
        response = QuestionTestCase.client.post(reverse("survey:create-question", kwargs={'questionnaire_slug': '2'}), {'title': 'Test Question 6', 'description': 'question description 6', 'help_text': 'question help text 6'}, follow=True)
        self.assertContains(response, "This field is required")

class QuestionnaireAPITestCase(TestCase):

        @classmethod
        def setUpTestData(cls):
            cls.client = login(user="question-user", email="question-user@example.com", password="password")

        def setUp(self):
            create_surveys()
            create_questionnaires()
            # first questionnaire has three questions
            Question.objects.create(title="Test Question 1", questionnaire=Questionnaire.objects.get(questionnaire_id='1'), description='question description 1', help_text='question help text 1', error_text='question error text 1')
            Question.objects.create(title="Test Question 2", questionnaire=Questionnaire.objects.get(questionnaire_id='1'), description='question description 2', help_text='question help text 2', error_text='question error text 2')
            Question.objects.create(title="Test Question 3", questionnaire=Questionnaire.objects.get(questionnaire_id='1'), description='question description 3', help_text='question help text 3', error_text='question error text 3')

            # whilst the second questionnaire has two questions
            Question.objects.create(title="Test Question 4", questionnaire=Questionnaire.objects.get(questionnaire_id='2'), description='question description 4', help_text='question help text 4', error_text='question error text 4')
            Question.objects.create(title="Test Question 5", questionnaire=Questionnaire.objects.get(questionnaire_id='2'), description='question description 5', help_text='question help text 5', error_text='question error text 5')

        def test_render_to_json_object_matches_schema(self):
            response = QuestionnaireAPITestCase.client.get(reverse("survey:questionnaire-api", kwargs={'slug': '1'}), follow=True)
            self.assertEqual(200, response.status_code)
            import json
            questionnaire = json.loads(response.content)
            self.assertEqual(3, len(questionnaire['questions']))
