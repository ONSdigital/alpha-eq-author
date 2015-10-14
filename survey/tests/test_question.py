from django.test import TestCase

from . import login


class QuestionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = login(user="question-user", email="question-user@example.com", password="password")

