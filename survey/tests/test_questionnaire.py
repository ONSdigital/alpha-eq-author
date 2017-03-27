import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from survey.models import Survey, Questionnaire
from . import create_surveys, create_questionnaires, login


class QuestionnaireTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = login(user="questionnaire-user", email="questionnaire-user@example.com", password="password")
        f = open('survey/tests/resources/survey.json')
        cls.contents = f.read()

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
        self.assertFalse(questionnaire1.reviewed)
        self.assertFalse(questionnaire2.reviewed)

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

    def test_reviewed(self):
        # add a new questionnaire to survey 1
        response = QuestionnaireTestCase.client.post(reverse("survey:create-questionnaire", kwargs={'survey_slug': '1'}), {'title' : 'Test Questionnaire 3', 'questionnaire_id': '3', 'overview': 'questionnaire overview 3'}, follow=True)
        self.assertEqual(200, response.status_code)

        # now check that survey 1 has two questionnaires and the reviewed state is correct
        response = QuestionnaireTestCase.client.get(reverse('survey:index'))
        survey = response.context['object_list'][0]
        self.assertEqual(Survey.objects.get(survey_id='1'), survey)
        questionnaire_set = survey.questionnaire_set.all()
        self.assertEqual(len(questionnaire_set), 2)
        self.assertEqual(Questionnaire.objects.get(questionnaire_id='3'), questionnaire_set[0])
        self.assertEqual(Questionnaire.objects.get(questionnaire_id='1'), questionnaire_set[1])
        self.assertFalse(questionnaire_set[0].reviewed)
        self.assertFalse(questionnaire_set[1].reviewed)

        questionnaire = Questionnaire.objects.get(questionnaire_id=1)
        response = QuestionnaireTestCase.client.get(reverse("survey:review-questionnaire", kwargs={'slug': questionnaire.id}), follow=True, HTTP_REFERER=reverse('survey:index'))

        questionnaire = Questionnaire.objects.get(questionnaire_id='1')
        self.assertTrue(questionnaire.reviewed)

    def test_reviewed_false_after_add_question(self):
        # add a new questionnaire to survey 1
        response = QuestionnaireTestCase.client.post(reverse("survey:create-questionnaire", kwargs={'survey_slug': '1'}), {'title' : 'Test Questionnaire 3', 'questionnaire_id': '3', 'overview': 'questionnaire overview 3'}, follow=True)
        self.assertEqual(200, response.status_code)

        questionnaire = Questionnaire.objects.get(questionnaire_id=3)
        response = QuestionnaireTestCase.client.get(reverse("survey:review-questionnaire", kwargs={'slug': questionnaire.id}), follow=True, HTTP_REFERER=reverse('survey:index'))
        questionnaire = Questionnaire.objects.get(questionnaire_id='3')
        self.assertTrue(questionnaire.reviewed)

        # check the reviewed status is true
        response = QuestionnaireTestCase.client.get(reverse('survey:index'))
        survey = response.context['object_list'][0]
        self.assertEqual(Survey.objects.get(survey_id='1'), survey)
        questionnaire_set = survey.questionnaire_set.all()
        self.assertTrue(questionnaire_set[0].reviewed)

        # now add a question
        response = QuestionnaireTestCase.client.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), QuestionnaireTestCase.contents,  content_type='Application/JSON', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertContains(response,"Your questionnaire has been saved")

        # and check the reviewed status is false
        response = QuestionnaireTestCase.client.get(reverse('survey:index'))
        survey = response.context['object_list'][0]
        self.assertEqual(Survey.objects.get(survey_id='1'), survey)
        questionnaire_set = survey.questionnaire_set.all()
        self.assertFalse(questionnaire_set[0].reviewed)

    def test_locked_questionnaire(self):
        # add a new questionnaire to survey 1
        response = QuestionnaireTestCase.client.post(reverse("survey:create-questionnaire", kwargs={'survey_slug': '1'}), {'title' : 'Test Questionnaire 3', 'questionnaire_id': '3', 'overview': 'questionnaire overview 3'}, follow=True)
        self.assertEqual(200, response.status_code)

        questionnaire = Questionnaire.objects.get(questionnaire_id=3)

        # lock the questionnaire
        response = QuestionnaireTestCase.client.get(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)

        # add a question to questionnaire
        response = QuestionnaireTestCase.client.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), QuestionnaireTestCase.contents,  content_type='Application/JSON', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertContains(response,"Your questionnaire has been saved")

        # log in as a new user
        new_user = login(user="new-user", email="new-user@example.com", password="password")

        # check we can't modify the questionnaire
        response = new_user.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), QuestionnaireTestCase.contents,  content_type='Application/JSON', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertContains(response,"Locked for editing")

    def test_unlocked_questionnaire(self):
        # add a new questionnaire to survey 1
        response = QuestionnaireTestCase.client.post(reverse("survey:create-questionnaire", kwargs={'survey_slug': '1'}), {'title' : 'Test Questionnaire 3', 'questionnaire_id': '3', 'overview': 'questionnaire overview 3'}, follow=True)
        self.assertEqual(200, response.status_code)

        questionnaire = Questionnaire.objects.get(questionnaire_id=3)

        # lock the questionnaire
        response = QuestionnaireTestCase.client.get(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)

        # add a question to questionnaire
        response = QuestionnaireTestCase.client.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), QuestionnaireTestCase.contents,  content_type='Application/JSON', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Your questionnaire has been saved")

        # log in as a new user
        new_user = login(user="new-user", email="new-user@example.com", password="password")

        # check we can't modify the questionnaire
        response = new_user.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), QuestionnaireTestCase.contents,  content_type='Application/JSON', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Locked for editing")

        # unlock the questionnaire
        response = QuestionnaireTestCase.client.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), '{"unlock":"true"}', content_type='Application/JSON', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Unlocked")

        # check the new user can modify it now
        response = new_user.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), QuestionnaireTestCase.contents,  content_type='Application/JSON', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Your questionnaire has been saved")

    def test_user_cannot_not_unlock_another_users_questionnaire(self):
        # add a new questionnaire to survey 1
        response = QuestionnaireTestCase.client.post(reverse("survey:create-questionnaire", kwargs={'survey_slug': '1'}), {'title' : 'Test Questionnaire 3', 'questionnaire_id': '3', 'overview': 'questionnaire overview 3'}, follow=True)
        self.assertEqual(200, response.status_code)

        questionnaire = Questionnaire.objects.get(questionnaire_id=3)

        # lock the questionnaire
        response = QuestionnaireTestCase.client.get(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)

        # add a question to questionnaire
        response = QuestionnaireTestCase.client.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), QuestionnaireTestCase.contents,  content_type='Application/JSON', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Your questionnaire has been saved")

        # log in as a new user
        new_user = login(user="new-user", email="new-user@example.com", password="password")

        # attempt to unlock the questionnaire
        response = new_user.post(reverse("survey:questionnaire-builder", kwargs={'pk': questionnaire.id}), '{"unlock":"true"}', content_type='Application/JSON', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Locked for editing")


